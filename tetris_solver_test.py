import TileSolver
import tetris_utils

problem = TileSolver.TileSolver(
    boardRows=3,
    boardCols=8,
    tiles=[TileSolver.LTile, TileSolver.ReverseLTile, TileSolver.LineTile, TileSolver.SquareTile,
           TileSolver.ZTile, TileSolver.STile],
    numTiles=[1, 1, 1, 1, 1, 1]
)

if problem.solveProblem():
    print("Found solution: ")
    TileSolver.printMatrix(problem.solutionBoard)
    indexes = []
    row_number = 0
    print("Found element L at : ")
    for row in problem.solutionBoard.tolist():
        index = tetris_utils.indices(row, 5, row_number)
        indexes.extend(index)
        row_number = row_number + 1
    print(indexes)
    print("Feasible points : ")
    f = tetris_utils.get_feasible_coordinates(indexes)
    print(f)
else:
    print("No solution found")
