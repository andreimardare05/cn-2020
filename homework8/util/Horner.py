def horner(x, poly):
    result = poly[0]
    for i in range(1, len(poly)):
        result *= x
        result += poly[i]

    return result
