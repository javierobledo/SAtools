import sys
from preprocessing import Preprocessing, ForbiddenAlgorithmException

if len(sys.argv) == 3:
    try:
        pre = Preprocessing(sys.argv[1],sys.argv[2])
    except ForbiddenAlgorithmException:
        print(sys.argv[2]+" not a valid algorithm")
    else:
        print(pre.run_algorithm())