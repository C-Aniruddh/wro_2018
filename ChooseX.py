import tetris_utils

solution = tetris_utils.solve_tetris()
# print(solution)

for i in solution:
    #print(i)
    pass

L=[]
def printMatrix2(mat):
    #print("===========================================================")
    L=[]
    for i in range(2,-1,-1):
        L1=[]
        for j in range(7,-1,-1):
            #print("\t%s" % mat[i][j], end="")
            L1.append(mat[i][j])
        L.append(L1)
        print(L1)
        #print("\n")
    print("===========================================================")
    return L
L=printMatrix2(solution)
#print(L)
#
# Z=[]
# S=[]
# I=[]
# J=[]
# L=[]
# O=[]

X=[[],[],[],[],[],[]]

for i in range(len(L)):
    for j in range(len(L[i])):
        x=L[i][j]-1
        #print("xxxxxxxxxxx",x)
        X[x].append([i,j])
print(X)

#print(i in X)

for i in X:
    print(i)

L0=X[1-1]
print("LLLLLLLLLL",L0)

coordinates = L0
sorted_coordinates_x = sorted(coordinates, key=lambda x: (-x[0], x[1]), reverse=False)
#sorted_coordinates_y = sorted(sorted_coordinates_x, key=lambda x: x[1], reverse=True)
print(sorted_coordinates_x)

world=[[5,0],[5,5],[5,10],[0,10]]

world2=[]

sorted_coordinates_y = sorted(world, key=lambda x: (-x[0], x[1]), reverse=False)
#sorted_coordinates_y = sorted(sorted_coordinates_x, key=lambda x: x[1], reverse=True)
print(sorted_coordinates_y)




