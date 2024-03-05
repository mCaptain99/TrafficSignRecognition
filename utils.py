

def is_close(x, y, threshold=10):
    return abs(x-y) < threshold


def check_if_y_coords_are_close(approx):
    return is_close(approx[0,0,1], approx[1,0,1]) or is_close(approx[0,0,1], approx[2,0,1]) or is_close(approx[1,0,1], approx[2,0,1])


def check_if_distances_are_close(approx):
    d1 = (approx[0, 0, 0] - approx[1, 0, 0])**2 + (approx[0, 0, 1] - approx[1, 0, 1])**2
    d2 = (approx[1, 0, 0] - approx[2, 0, 0])**2 + (approx[1, 0, 1] - approx[2, 0, 1])**2
    d3 = (approx[0, 0, 0] - approx[2, 0, 0])**2 + (approx[0, 0, 1] - approx[2, 0, 1])**2
    return d1 > 200 and d2 > 200 and d3 > 200 and d1 < 1600 and d2 < 1600 and d3 < 1600 and \
           is_close(d1, d2, threshold=50) and is_close(d2, d3, threshold=50)


def check_x_coord_distance(approx):
    return is_close(abs(approx[0, 0, 0] - approx[1, 0, 0]), abs(approx[0, 0, 0] - approx[2, 0, 0]), threshold=20) or \
           is_close(abs(approx[0, 0, 0] - approx[1, 0, 0]), abs(approx[1, 0, 0] - approx[2, 0, 0]), threshold=20) or \
           is_close(abs(approx[0, 0, 0] - approx[2, 0, 0]), abs(approx[1, 0, 0] - approx[2, 0, 0]), threshold=20)


def check_if_triangle(approx):
    try:
        return check_if_y_coords_are_close(approx) and check_if_distances_are_close(approx) and check_x_coord_distance(approx)
    except:
        return False


def get_triangle_frame(approx, thresh=5):
    x0 = min(approx[0, 0, 0], approx[1, 0, 0], approx[2, 0, 0]) - thresh
    x1 = max(approx[0, 0, 0], approx[1, 0, 0], approx[2, 0, 0]) + thresh
    y0 = min(approx[0, 0, 1], approx[1, 0, 1], approx[2, 0, 1]) - thresh
    y1 = max(approx[0, 0, 1], approx[1, 0, 1], approx[2, 0, 1]) + thresh
    return x0, y0, x1, y1


def check_if_coords_x_are_close_in_square(approx):
    return (is_close(approx[0, 0, 0], approx[1, 0, 0]) and is_close(approx[2, 0, 0], approx[3, 0, 0])) \
           or (is_close(approx[0, 0, 0], approx[2, 0, 0]) and is_close(approx[1, 0, 0], approx[3, 0, 0])) \
           or (is_close(approx[0, 0, 0], approx[3, 0, 0]) and is_close(approx[1, 0, 0], approx[2, 0, 0]))


def check_if_coords_y_are_close_in_square(approx):
    return (is_close(approx[0, 0, 1], approx[1, 0, 1]) and is_close(approx[2, 0, 1], approx[3, 0, 1])) \
           or (is_close(approx[0, 0, 1], approx[2, 0, 1]) and is_close(approx[1, 0, 1], approx[3, 0, 1])) \
           or (is_close(approx[0, 0, 1], approx[3, 0, 1]) and is_close(approx[1, 0, 1], approx[2, 0, 1]))


def check_if_distances_are_close_in_square(approx):
    d1 = (approx[0, 0, 0] - approx[1, 0, 0])**2 + (approx[0, 0, 1] - approx[1, 0, 1])**2
    d2 = (approx[1, 0, 0] - approx[2, 0, 0])**2 + (approx[1, 0, 1] - approx[2, 0, 1])**2
    d3 = (approx[0, 0, 0] - approx[2, 0, 0])**2 + (approx[0, 0, 1] - approx[2, 0, 1])**2
    d4 = (approx[0, 0, 0] - approx[3, 0, 0])**2 + (approx[0, 0, 1] - approx[3, 0, 1])**2
    d5 = (approx[1, 0, 0] - approx[3, 0, 0])**2 + (approx[1, 0, 1] - approx[3, 0, 1])**2
    d6 = (approx[2, 0, 0] - approx[3, 0, 0])**2 + (approx[2, 0, 1] - approx[3, 0, 1])**2
    return d1 > 200 and d2 > 200 and d3 > 200 and d1 < 1600 and d2 < 1600 and d3 < 1600 and \
           d4 > 200 and d5 > 200 and d6 > 200 and d4 < 1600 and d5 < 1600 and d6 < 1600 and \
           (is_close(d1,d2) and is_close(d2, d3) and is_close(d3,d4) and is_close(d4,d1)) or \
           (is_close(d1,d5) and is_close(d5, d3) and is_close(d3,d4) and is_close(d4,d1)) or \
           (is_close(d1,d6) and is_close(d6, d3) and is_close(d3,d4) and is_close(d4,d1)) or \
           (is_close(d5,d2) and is_close(d2, d3) and is_close(d3,d4) and is_close(d4,d5)) or \
           (is_close(d6,d2) and is_close(d2, d3) and is_close(d3,d4) and is_close(d4,d6)) or \
           (is_close(d1,d2) and is_close(d2, d5) and is_close(d5,d4) and is_close(d4,d1)) or \
           (is_close(d1,d2) and is_close(d2, d6) and is_close(d6,d4) and is_close(d4,d1)) or \
           (is_close(d1,d2) and is_close(d2, d3) and is_close(d3,d5) and is_close(d5,d1)) or \
           (is_close(d1,d2) and is_close(d2, d3) and is_close(d3,d6) and is_close(d6,d1))


def check_if_square(approx):
    return check_if_distances_are_close_in_square(approx) and check_if_coords_x_are_close_in_square(approx) and \
           check_if_coords_y_are_close_in_square(approx)


def get_square_frame(approx, thresh=5):
    x0 = min(approx[0, 0, 0], approx[1, 0, 0], approx[2, 0, 0], approx[3, 0, 0]) - thresh
    x1 = max(approx[0, 0, 0], approx[1, 0, 0], approx[2, 0, 0], approx[3, 0, 0]) + thresh
    y0 = min(approx[0, 0, 1], approx[1, 0, 1], approx[2, 0, 1], approx[3, 0, 1]) - thresh
    y1 = max(approx[0, 0, 1], approx[1, 0, 1], approx[2, 0, 1], approx[3, 0, 1]) + thresh
    return x0, y0, x1, y1
