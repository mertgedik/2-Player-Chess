import time

import numpy as np

arr = np.zeros((3,3,3))
arr[0,0,0] = 5
arr[1,1,1] = 3
arr[2,2,2] = 4
arr = np.append(arr,np.zeros((3,3,1)),axis=2)

print(arr)