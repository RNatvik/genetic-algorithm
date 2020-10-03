def lin_map(x, x0, x1, y0, y1):
    y = x * (y1 - y0) / (x1 - x0) + y0
    return y
