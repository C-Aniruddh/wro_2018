import TileSolver

problem = TileSolver.TileSolver(
    boardRows=3,
    boardCols=8,
    tiles=[TileSolver.LTile, TileSolver.ReverseLTile, TileSolver.LineTile, TileSolver.SquareTile,
           TileSolver.ZTile, TileSolver.STile],
    numTiles=[1, 1, 1, 1, 1, 1]
)


def solve_tetris():
    if problem.solveProblem():
        TileSolver.printMatrix(problem.solutionBoard)
        return problem.solutionBoard.tolist()


def get_block_id(shape):
    if shape == "L":
        return 1
    elif shape == "Inv-L":
        return 2
    elif shape == "I":
        return 3
    elif shape == "O":
        return 4
    elif shape == "Z":
        return 5
    elif shape == "S":
        return 6


def indices(lst, element, row_number):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset + 1)
            offset_a = [row_number, offset]
        except ValueError:
            return result
        result.append(offset_a)


def get_feasible_coordinates(in_list):
    feasible = []
    feasible2=[]
    for element in in_list:
        if 2 <= element[1] <= 5:
            feasible.append(element)
            feasible2.append([2-element[0],7-element[1]])
    return feasible2
