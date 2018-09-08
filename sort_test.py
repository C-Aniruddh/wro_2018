coordinates = [[0, 0], [1, 2], [1, 1], [1, 0]]  # list of [x, y]
sorted_coordinates_x = sorted(coordinates, key=lambda x: (-x[0], x[1]), reverse=False)
#sorted_coordinates_y = sorted(sorted_coordinates_x, key=lambda x: x[1], reverse=True)
print(sorted_coordinates_x)
