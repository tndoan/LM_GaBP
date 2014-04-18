import numpy as np
import sys

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

def construct_neighbor(A):
    """return dict whose key is the variable id,
    value is the list of its neighbors. 
    j is neighbor of i if A[i][j] != 0"""
    result = dict()
    size = A.shape[0] # number of variable in
    for i in range(size):
        for j in range(size):
            if A[i][j] != 0:
                neighbors = result.get(i)
                if neighbors == None:
                    result[i] = [j]
                else:
                    neighbors.append(j)
    return result

if __name__ == "__main__":
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    threshold = 0.01
    A = np.loadtxt(filename1, delimiter=' ')
    b = np.loadtxt(filename2)

    # check symmetric of matrix A
    if not is_satisfied(A, b):
        print "The matrix and vector from input are not valid"
        return

    # initialization
    mean = np.zeros(A.shape[0])
    precision = np.ones(A.shape[0])
    neighbors = construct_neighbor(A)

    # solve the symmetric case
