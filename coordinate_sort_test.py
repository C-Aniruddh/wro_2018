coordinates = [[0, 3], [1, 2], [3, 4], [5, 2]]  # list of [x, y]
sorted_coordinates = sorted(coordinates, key=lambda x: x[1], reverse=True)
print(sorted_coordinates)
