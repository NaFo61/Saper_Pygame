def generate_neighbors(square):
    """ Возвращает клетки соседствующие с square """
    if square == 0:
        data = (1, 11, 10)
    elif square == 9:
        data = (8, 18, 19)
    elif square == 90:
        data = (80, 81, 91)
    elif square == 99:
        data = (89, 88, 98)

    elif square in (1, 2, 3, 4, 5, 6, 7, 8):
        data = (
            square - 1, square - 1 + 10, square + 10, square + 1 + 10,
            square + 1)
    elif square in (91, 92, 93, 94, 95, 96, 97, 98):
        data = (
            square - 1, square - 1 - 10, square - 10, square + 1 - 10,
            square + 1)
    elif square in (10, 20, 30, 40, 50, 60, 70, 80):
        data = (
            square - 10, square + 1 - 10, square + 1, square + 1 + 10,
            square + 10)
    elif square in (19, 29, 39, 49, 59, 69, 79, 89):
        data = (
            square - 10, square - 10 - 1, square - 1, square - 1 + 10,
            square + 10)
    else:
        data = (
            square - 1 - 10, square - 10, square + 1 - 10, square + 1,
            square + 1 + 10, square + 10, square - 1 + 10, square - 1)
    return data
gog = generate_neighbors(23)
print(gog)

