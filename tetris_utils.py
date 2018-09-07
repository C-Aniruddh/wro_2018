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
    for element in in_list:
        if 2 <= element[1] <= 5:
            feasible.append(element)
    return feasible
