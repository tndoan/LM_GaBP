import numpy as np
import sys
import networkx as nx

def is_satisfied(A, b):
    """check condition of matrix A and vector b:
    A is the symmetric matrix and the size of A is equal to b"""
    # check symmetric property of A
    if not (A == A.T).all():
        return False
    
    # check the size of A and b
    if not (A.shape[0] == A.shape[1] == b.shape[0]):
        return False
    return True

def construct_graph(A, b):
    """return dict whose key is the variable id,
    value is the list of its neighbors. 
    j is neighbor of i if A[i][j] != 0"""
    result = nx.DiGraph()
    size = A.shape[0]
    
    # initialize prior and marginal distribution for each node
    # mean and prec is the parameters of marginal distribution
    for i in range(size):
        # prior is equivalent to phi function in paper
        result.add_node(i, prior_mean=float(b[i])/A[i][i], prior_precision=float(A[i][i]),\
                mean=0.0, prec=0.0) 
    
    # initialize the distribution of message between 2 nodes
    # g[i][j] = message from i to j. It is Gaussian distribution
    for i in range(size):
        for j in range(size):
            if A[i][j] != 0 and i != j: # add if the value is not zero
                result.add_edge(i, j, mean=0.0, precision=0.0)
    return result

def check_continue(old_graph, graph, threshold):
    """there are not specific condition for this part. 
    But this terminates if the sum of mean difference of nodes in
    old graph and new graph is less than the threshold"""
    nodes = graph.nodes()
    total_difference = 0.0
    for i in nodes:
        difference = abs(old_graph.node[i]['mean'] - graph.node[i]['mean'])
        total_difference += difference
    if total_difference < threshold:
        return False # the total sum is less than threshold
    return True

def iterate_until_convergence(graph, threshold, A):
    """iteration through graph to find the solution"""
    isContinue = True
    nodes = graph.nodes() # set of nodes in graph
    count = 0 # count the number of iteration

    # run untial 1000 iterations or convergence
    while isContinue and count < 1000:
        old_graph = graph.copy()
        
        # update the marginal distribution of each node
        for i in nodes:
            node_info = graph.node[i]
            graph.node[i]['prec'] = graph.node[i]['prior_precision']
            temp = 0.0
            for j in nodes:
                neighbor = graph[i].get(j) 
                if neighbor != None: # it is actual neighbor
                    graph.node[i]['prec'] += graph[j][i]['precision']
                    temp += graph[j][i]['mean'] * graph[j][i]['precision']
            graph.node[i]['mean'] = (1.0/graph.node[i]['prec']) \
                    * (graph.node[i]['prior_mean'] * graph.node[i]['prior_precision'] + temp)

        # update the distribution of message
        for i in nodes:
            for j in nodes:
                node_info = graph[i].get(j)
                if node_info != None:
                    graph[i][j]['precision'] = -float(A[i][j]) * float(A[i][j]) /(graph.node[i]['prec'] - graph[j][i]['precision'])
                    graph[i][j]['mean'] = (graph.node[i]['prec'] * graph.node[i]['mean'] \
                            - graph[j][i]['precision'] * graph[j][i]['mean'])/float(A[i][j])
        isContinue = check_continue(old_graph, graph, threshold)
        count += 1
    return graph

if __name__ == "__main__":
    """solve the problem A x = b using probabilistic graphical model"""
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    threshold = 0.01
    A = np.loadtxt(filename1, delimiter=' ')
    b = np.loadtxt(filename2)

    # check symmetric of matrix A
    if not is_satisfied(A, b):
        print "The matrix and vector from input are not valid"
        sys.exit(0)

    graph = construct_graph(A, b) # initialization
  
    # iterate to solve
    result_graph = iterate_until_convergence(graph, threshold, A)

    # print result 
    nodes = result_graph.nodes()
    for i in nodes:
        print result_graph.node[i]['mean']
