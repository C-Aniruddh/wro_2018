import tetris_utils


def get_correct_hole(world_coordinates, feasible_coordinate):
    solution = tetris_utils.solve_tetris()
    # print(solution)

    for i in solution:
        # print(i)
        pass

    L = []

    def printMatrix2(mat):
        L = []
        for i in range(2, -1, -1):
            L1 = []
            for j in range(7, -1, -1):
                L1.append(mat[i][j])
            L.append(L1)
            print(L1)
            # print("\n")
        return L

    L = printMatrix2(solution)

    X = [[], [], [], [], [], []]

    for i in range(len(L)):
        for j in range(len(L[i])):
            x = L[i][j] - 1
            X[x].append([i, j])

    for i in X:
        # print(i)
        pass

    L0 = X[1 - 1]
    print("\nOriginal matrix co-ordinates list: ", L0)

    coordinates = L0
    sorted_coordinates_x = sorted(coordinates, key=lambda x: (-x[0], x[1]), reverse=False)
    # sorted_coordinates_y = sorted(sorted_coordinates_x, key=lambda x: x[1], reverse=True)
    print("Sorted matrix co-ordinates list: ", sorted_coordinates_x)

    # Conerting wrt the refernce

    matrix = sorted_coordinates_x
    reference = matrix[0]

    ref_x = reference[0]
    ref_y = reference[1]

    for i in matrix:
        i[0] = i[0] - ref_x
        i[1] = i[1] - ref_y
    print("\nReference for matrix: ", reference)
    print("Our converted matrix co-ord: ", matrix)

    # feasible_coordinate = feasible_coordinates[0]
    print("\nFeasible co-ordinate: ", feasible_coordinate, "(1 th element of the above)")

    index = -1

    for i in range(len(matrix)):
        if matrix[i] == feasible_coordinate:
            index = i

    print("The", index, "th element of the world co-ordinate matrix is what we need\n")

    world = world_coordinates
    print("Original world co-ordinates list: ", world)
    # Swap x,y
    worldx = world
    for i in world:
        x = i[0]
        y = i[1] * (-1)
        i[0] = y
        i[1] = x  # I KNOW HOW TO DO THIS IN ONE LINE ALSO (just trying to make things more clear to ppl)

    worldX = world
    world2 = []
    sorted_coordinates_y = sorted(world, key=lambda x: (-x[0], x[1]), reverse=False)

    # sorted_coordinates_y = sorted(sorted_coordinates_x, key=lambda x: x[1], reverse=True)
    print("Sorted world co-ordinates list: ", sorted_coordinates_y)

    sorted_w = sorted_coordinates_y
    # Converting wrt a reference

    world2 = world

    reference_w = world2[0]
    ref_w_x = reference_w[0]
    ref_w_y = reference_w[1]

    world_original = []
    world_round = []
    for i in world2:
        world_original.append([i[0], i[1]])
        i[0] = i[0] - ref_w_x
        i[1] = i[1] - ref_w_y
        world_round.append([round(i[0]), round(i[1])])

    world3 = []
    for i in world_round:
        world3.append([int(i[0] / 5), int(i[1] / 5)])
    print("\nReference for matrix: ", reference_w)
    print("Sorted world co-ordinates list: ", world_original)
    print("\nWorld co-ordinate wrt to the reference: ", world2)  # Coordinates wrt reference

    print("Our converted world co-ord (divide the above by 5): ", world3)
    y = world_original[index]
    print("\nRequired hole (", index, "th element ): ", y)
    return y
