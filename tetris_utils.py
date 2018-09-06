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


def get_coordinates(input_tile, solution_matrix):
    indexes = list(solution_matrix).index(input_tile)
    return indexes
