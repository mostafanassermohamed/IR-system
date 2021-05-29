import random
list_of_chars = ['A', 'B', 'C', 'D', 'E', 'F' , '1', '2', '3', '4', '5']
list_of_doc = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']                                           
for k in list_of_doc:
    random_size = random.randint(3,10)
    temp = []
    for i in range(random_size):
        st = random.choice(''.join(list_of_chars))
        temp.append(st)
    open(k, "r+").write(''.join(temp))

import numpy as np

adj_matrix=np.zeros((5,5))
for a in list_of_doc:
    tmp=open(a,'r').readlines()
    for b in range(5):
        if (str(b+1) in str(tmp)) and ((b) != list_of_doc.index(a)) : # ignore looooops
            adj_matrix[list_of_doc.index(a)][b]=1
adj_matrix_T=np.transpose(adj_matrix)
a=np.array([[1,1,1,1,1]]).T
h=a
print('initial a,h =', a,h)
print("adj matrix",adj_matrix)
print("adj matrix transpose",adj_matrix_T)

for i in range(20):
    a=np.dot(adj_matrix_T,h)
    h=np.dot(adj_matrix,a)
a=np.array(a).tolist()
h=np.array(h).tolist()
print('Authority =',a)
print('Hubs=',h)
result={}
for i in range(5):
     result.update({list_of_doc[i]:a[i]})
L1=sorted (result.items(), key=lambda i:(i[1], i[0]), reverse=True) 
print(L1)