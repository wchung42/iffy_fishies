from random import randrange

# Calculate slope
def calc_slope(p1, p2):
    '''Inputs: p1 and p2 (x, y) tuples; Returns slope'''
    return (p2[1] - p1[1]) / (p2[0] - p1[0])

# Calculate y-intercept
def calc_yintercept(p, m):
    '''Inputs: p (x, y) tuple and m slope; Returns y-intercept'''
    return p[1] - (m * p[0])

def rand_color():
    '''Returns a random RGB tuple'''
    
    return (randrange(0, 256), randrange(0, 256), randrange(0, 256), 255)

def rand_coor(x1, x2, y1, y2):
    '''Generates a random x and random y within given range and Returns a random (x,y) tuple'''
    
    return (randrange(x1, x2), (randrange(y1, y2)))