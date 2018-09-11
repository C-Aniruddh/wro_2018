unit=1
coordinates = [[1, 0], [1, 1], [0, 1], [0, 2]]  # list of [x, y]
sorted_coordinates_x = sorted(coordinates, key=lambda x: (x[0]), reverse=False)
#sorted_coordinates_y = sorted(sorted_coordinates_x, key=lambda x: x[1], reverse=True)
print(sorted_coordinates_x)

l0=[]
l1=[]
l2=[]
l3=[]

for i in sorted_coordinates_x:
    if i[0]==0:
        l0.append(i)
    if i[0]==1:
        l1.append(i)
    if i[0]==2:
        l2.append(i)
    if i[0]==3:
        l3.append(i)

print(l0,"\t",l1,"\t",l2,"\t",l3)

print(l3,"\t",l2,"\t",l1,"\t",l0)