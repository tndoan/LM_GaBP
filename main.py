import numpy as np
import sys

if __name__ == "__main__":
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    A = np.loadtxt(filename1, delimiter=' ')
    b = np.loadtxt(filename2)

    # check symmetric of matrix A
    if not (A == A.T).all():
        print "matrix A is not symmetric. Cannot solve"
        return

    # solve the symmetric case
