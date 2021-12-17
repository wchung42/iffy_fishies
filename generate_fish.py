'''
#TeamSeas

 - Generate Tangram Fish with PIL; 1 of 5 designs
 - Scale and transform based on donation and randomness
 - Make background transparent
 - Save image
 - Overlay onto main canvas

'''

from PIL import Image, ImageDraw
from random import randrange
from util import *
import math

def transform(img, rotate_range):
    '''Rotates within rotate_range, flips image and scales image; Returns the resulting image'''
    start, end =  rotate_range
    result = img.rotate(randrange(start, end))
    
    if randrange(0, 5) == 1:
        result = result.transpose(method=Image.FLIP_LEFT_RIGHT)
        
    return result

def resize(img, size_multiplier=1):
    '''Returns resized image'''
    resized_img = img.resize((round(1000*size_multiplier), round(1000*size_multiplier)), resample=Image.ANTIALIAS)

    return resized_img

def calc_scale_multiplier(val):
    '''Convert given val to a scaling multiplier'''
    if val >= 750:
        val = 750
    
    multiplier = val/1000
    
    if multiplier < 0.075:    
        return 0.075
    else:
        return multiplier

# ---------------------------- Iffy Fishy Generation Functions ------------------------------- #

def draw_fish_design_1(**kwargs):
    '''Generate fish with design #1'''
    if kwargs.get('color') is not None:
        bg_color = kwargs.get('color')
    else:
        bg_color = (0, 0, 0, 0)

    img = Image.new('RGBA', (1000, 1000), bg_color)

    draw = ImageDraw.Draw(img)
    
    # head - triangle a
    head_triangle_a_bl = rand_coor(125, 175, 475, 525)
    head_triangle_a_bl_x, head_triangle_a_bl_y = head_triangle_a_bl
    head_triangle_a_tp = (head_triangle_a_bl_x + randrange(250, 315), head_triangle_a_bl_y - randrange(225, 325))
    head_triangle_a_br = (head_triangle_a_bl_x + randrange(250, 315), head_triangle_a_bl_y + randrange(-25, 25))
    draw.polygon([head_triangle_a_bl, head_triangle_a_tp, head_triangle_a_br], fill=rand_color(), outline='black')

    # head - triangle b 
    head_triangle_b_tpl = head_triangle_a_bl
    head_triangle_b_tpr = head_triangle_a_br
    head_triangle_b_tpl_x, head_triangle_b_tpl_y = head_triangle_b_tpl
    head_triangle_b_btm = (head_triangle_b_tpl_x + randrange(250, 315), head_triangle_b_tpl_y + randrange(225, 325))
    draw.polygon([head_triangle_b_tpl, head_triangle_b_tpr, head_triangle_b_btm], fill=rand_color(), outline='black')

    # body - rhombus
    m = calc_slope(head_triangle_b_tpr, head_triangle_b_btm) # calculate slope and y-intercept of head_triangle_b to find tpr and btmr points of rhombus
    b = calc_yintercept(head_triangle_b_tpr, m)

    rhombus_tpl_y = randrange(math.floor(head_triangle_b_tpr[1] * 1.05), math.floor(head_triangle_b_tpr[1] * 1.1)) # find y along the side of the triangle
    rhombus_tpl_x = head_triangle_b_tpr[0] if m == 0 else math.floor((rhombus_tpl_y - b) / m) # if vertical, x == x of triangle
    rhombus_tpl = (rhombus_tpl_x, rhombus_tpl_y)

    rhombus_btml_y = randrange(math.floor(head_triangle_b_tpr[1] * 1.35), math.floor(head_triangle_b_tpr[1] * 1.4))
    rhombus_btml_x = head_triangle_b_tpr[0] if m == 0 else math.floor((rhombus_btml_y - b) / m)# if vertical, x == x of triangle
    rhombus_btml = (rhombus_btml_x, rhombus_btml_y)

    # top right point with respect to top left point of rhombus
    rhombus_tpr = (randrange(rhombus_tpl_x + 100, rhombus_tpl_x + 165), randrange(rhombus_tpl_y - 100, rhombus_tpl_y - 45))
    rhombus_btmr = (randrange(rhombus_tpl_x + 100, rhombus_tpl_x + 165), randrange(rhombus_tpl_y + 45, rhombus_tpl_y + 100))
    draw.polygon([rhombus_tpl, rhombus_btml, rhombus_btmr, rhombus_tpr], fill=rand_color(), outline='black')

    # body - triangle
    body_triangle_btm = rhombus_tpl
    body_triangle_midl = head_triangle_a_br
    body_triangle_midr = rhombus_tpr

    m = calc_slope(head_triangle_a_tp, head_triangle_a_br)
    b = calc_yintercept(head_triangle_a_tp, m)

    body_triangle_tp_y = randrange(math.floor(head_triangle_a_tp[1] * 1.2), math.floor(head_triangle_a_tp[1] * 1.3))
    body_triangle_tp_x = head_triangle_a_tp[0] if m == 0 else math.floor((body_triangle_tp_y - b) / m)
    body_triangle_tp = (body_triangle_tp_x, body_triangle_tp_y)
    draw.polygon([body_triangle_tp, body_triangle_midl, body_triangle_btm, body_triangle_midr], fill=rand_color(), outline='black')

    # tail - square 
    tail_square_tpl = rhombus_tpr
    tail_square_btml = rhombus_btmr
    tail_square_btmr = (randrange(tail_square_btml[0] + 75, tail_square_btml[0] + 126), randrange(tail_square_btml[1] - 45, tail_square_btml[1] + 45))
    tail_square_tpr = (randrange(tail_square_tpl[0] + 75, tail_square_tpl[0] + 126), randrange(tail_square_tpl[1] - 45, tail_square_tpl[1] + 45))
    draw.polygon([tail_square_tpl, tail_square_btml, tail_square_btmr, tail_square_tpr], fill=rand_color(), outline='black')

    # tail - triangle a
    tail_triangle_a_btml = tail_square_tpl
    tail_triangle_a_btmr = tail_square_tpr
    tail_triangle_a_tp = (randrange(tail_triangle_a_btmr[0] - 25, tail_triangle_a_btmr[0] + 50), randrange(tail_triangle_a_btmr[1] - 150, tail_triangle_a_btmr[1] - 75))
    draw.polygon([tail_triangle_a_btml, tail_triangle_a_btmr, tail_triangle_a_tp], fill=rand_color(), outline='black')

    # tail - triangle b
    tail_triangle_b_tpl = tail_square_btml
    tail_triangle_b_tpr = tail_square_btmr
    tail_triangle_b_btm = (randrange(tail_triangle_b_tpr[0] - 25, tail_triangle_b_tpr[0] + 50), randrange(tail_triangle_b_tpr[1] + 75, tail_triangle_b_tpr[1] + 150))
    draw.polygon([tail_triangle_b_tpl, tail_triangle_b_tpr, tail_triangle_b_btm], fill=rand_color(), outline='black')

    return img


def draw_fish_design_2(**kwargs):
    '''Generate fish with design #2'''
    if kwargs.get('color') is not None:
        bg_color = kwargs.get('color')
    else:
        bg_color = (0, 0, 0, 0)

    img = Image.new('RGBA', (1000, 1000), bg_color)
    
    draw = ImageDraw.Draw(img)
    
    square_top_left = rand_coor(700, 750, 475, 525)
    square_top_left_x, square_top_left_y = square_top_left
    square_top_right = (square_top_left_x + randrange(83, 167), square_top_left_y + randrange(0, 83))
    square_bottom_right = (square_top_left_x + randrange(83, 166), square_top_left_y + randrange(83, 167))
    square_bottom_left = (square_top_left_x + randrange(-50, 83), square_top_left_y + randrange(83, 167))
    draw.polygon([square_top_left, square_top_right, square_bottom_right, square_bottom_left], fill=rand_color(), outline='black')
    
    # head - triangle using square_top_left and square_top_right
    head_triangle_top = (square_top_left_x, square_top_left_y - randrange(83, 167))
    draw.polygon([head_triangle_top, square_top_right, square_top_left], fill=rand_color(), outline='black')

    # body - triangleish a using square_top_left, square_bottom_left, head_triangle_top
    body_triangleish_a_top = (square_top_left_x - randrange(139, 278), square_top_left_y - randrange(83, 167))
    # body_triangleish_a_top_right = head_triangle_top
    # body_triangelish_a_bottom_right = square_bottom_left
    draw.polygon([body_triangleish_a_top, head_triangle_top, square_top_left, square_bottom_left], fill=rand_color(), outline='black')
    
    # body - triangleish b using body_triangleish_a_top
    # find point on hypotenuse of body_triangleish_a_top
    m = calc_slope(body_triangleish_a_top, square_bottom_left)
    y = randrange(square_top_left_y, square_bottom_left[1] + 1)
    x = (y - calc_yintercept(body_triangleish_a_top, m)) / m

    body_triangleish_b_bottom_right = (x, y)
    body_triangleish_b_bottom_left = (body_triangleish_a_top[0] - randrange(98, 197), body_triangleish_a_top[1] + randrange(98, 197)) # get bottom left point with respect to body_triangleish_a_top
    draw.polygon([body_triangleish_a_top, body_triangleish_b_bottom_right, body_triangleish_b_bottom_left], fill=rand_color(), outline='black')

    # bottom fin - triangleish with respect to body_triangleish_b_bottom_right
    bottom_fin_right = (body_triangleish_b_bottom_right[0] - randrange(0, 42), body_triangleish_b_bottom_right[1] + randrange(83, 167))
    bottom_fin_left = (body_triangleish_b_bottom_right[0] - randrange(84, 167), body_triangleish_b_bottom_right[1] + randrange(84, 167))
    draw.polygon([body_triangleish_b_bottom_right, bottom_fin_right, bottom_fin_left], fill=rand_color(), outline='black')

    # top fin - rhombus with respect to head_triangle_top
    top_fin_bl = (head_triangle_top[0] - randrange(90, 139), head_triangle_top[1] - randrange(25, 75))
    top_fin_tl = (head_triangle_top[0] - randrange(75, 125), head_triangle_top[1] - randrange(100, 150))
    top_fin_tr = (head_triangle_top[0] - randrange(25, 45), head_triangle_top[1] - randrange(75, 125))
    draw.polygon([head_triangle_top, top_fin_bl, top_fin_tl, top_fin_tr], fill=rand_color(), outline='black')

    # tail - triangle with respect to body_triangleish_b_bottom_left
    tail_top = (body_triangleish_b_bottom_left[0] - randrange(35, 100), body_triangleish_b_bottom_left[1] - randrange(35, 100))
    tail_bottom = (body_triangleish_b_bottom_left[0] - randrange(35, 100), body_triangleish_b_bottom_left[1] + randrange(35, 100))
    draw.polygon([body_triangleish_b_bottom_left, tail_top, tail_bottom], fill=rand_color(), outline='black')

    return img


def draw_fish_design_3(**kwargs):
    '''Generate fish with design #3'''
    if kwargs.get('color') is not None:
        bg_color = kwargs.get('color')
    else:
        bg_color = (0, 0, 0, 0)

    img = Image.new('RGBA', (1000, 1000), bg_color)
    
    draw = ImageDraw.Draw(img)
    
    # head - triangle
    head_triangle_mid = rand_coor(750, 801, 450, 550)
    head_triangle_tp = (randrange(head_triangle_mid[0] - 200, head_triangle_mid[0] - 150), randrange(head_triangle_mid[1] - 125, head_triangle_mid[1] - 75))
    head_triangle_btm = (randrange(head_triangle_mid[0] - 200, head_triangle_mid[0] - 150), randrange(head_triangle_mid[1] + 75, head_triangle_mid[1] + 125))
    draw.polygon([head_triangle_mid, head_triangle_tp, head_triangle_btm], fill=rand_color(), outline='black')

    # body - triangle
    body_triangle_tp = head_triangle_tp
    body_triangle_btm = head_triangle_btm
    body_triangle_mid = (randrange(head_triangle_tp[0] - 275, head_triangle_tp[0] - 200), randrange(head_triangle_tp[1] + 75, head_triangle_tp[1] + 125))
    draw.polygon([body_triangle_tp, body_triangle_btm, body_triangle_mid], fill=rand_color(), outline='black')

    # tail -  triangle
    tail_mid =  body_triangle_mid
    tail_tp = (randrange(tail_mid[0] - 75, tail_mid[0] - 50), randrange(tail_mid[1] - 75, tail_mid[1] - 50))
    tail_btm = (randrange(tail_mid[0] - 75, tail_mid[0] - 50), randrange(tail_mid[1] + 50, tail_mid[1] + 75))
    draw.polygon([tail_mid, tail_tp, tail_btm], fill=rand_color(), outline='black')

    # bottom fin - square 
    m = calc_slope(body_triangle_btm, body_triangle_mid)
    b = calc_yintercept(body_triangle_btm, m)

    x = randrange(body_triangle_mid[0] + 135, body_triangle_mid[0] + 150)
    y = (m * x) + b

    lower_fin_square_tp = (x, y)
    lower_fin_square_midr = body_triangle_btm
    lower_fin_square_midl = (randrange(lower_fin_square_midr[0] - 125, lower_fin_square_midr[0] - 100), randrange(lower_fin_square_midr[1], lower_fin_square_midr[1] + 75))
    lower_fin_square_btm = (randrange(lower_fin_square_midr[0] - 50, lower_fin_square_midr[0] - 25), randrange(lower_fin_square_midr[1] + 50, lower_fin_square_midr[1] + 75))
    draw.polygon([lower_fin_square_tp, lower_fin_square_midr, lower_fin_square_btm, lower_fin_square_midl], fill=rand_color(), outline='black')

    # bottom fin - triangle
    lower_fin_triangle_tp = lower_fin_square_midl
    lower_fin_triangle_mid = lower_fin_square_btm
    lower_fin_triangle_btm = (randrange(lower_fin_triangle_tp[0] - 35, lower_fin_triangle_tp[0] + 15), randrange(lower_fin_triangle_tp[1] + 50, lower_fin_triangle_tp[1] + 100))
    draw.polygon([lower_fin_triangle_tp, lower_fin_triangle_mid, lower_fin_triangle_btm], fill=rand_color(), outline='black')

    # top fin - triangle
    m = calc_slope(body_triangle_tp, body_triangle_mid)
    b = calc_yintercept(body_triangle_tp, m)

    x = randrange(body_triangle_tp[0] - 100, body_triangle_tp[0] - 50)
    y =  math.floor((m * x) + b)

    upper_fin_triangle_btm = (x, y)
    upper_fin_triangle_mid = body_triangle_tp
    upper_fin_triangle_tp = (randrange(upper_fin_triangle_btm[0] - 50, upper_fin_triangle_btm[0] + 10), randrange(upper_fin_triangle_btm[1] - 125, upper_fin_triangle_btm[1] - 75))
    draw.polygon([upper_fin_triangle_btm, upper_fin_triangle_tp, upper_fin_triangle_mid], fill=rand_color(), outline='black')

    # upper fin - triangle b
    upper_fin_triangle_b_br = upper_fin_triangle_btm
    upper_fin_triangle_b_tr = upper_fin_triangle_tp
    upper_fin_triangle_b_tl = (randrange(upper_fin_triangle_b_tr[0] - 100, upper_fin_triangle_b_tr[0] - 75), randrange(upper_fin_triangle_b_tr[1] - 75, upper_fin_triangle_b_tr[1] - 50))
    draw.polygon([upper_fin_triangle_b_br, upper_fin_triangle_b_tr, upper_fin_triangle_b_tl], fill=rand_color(), outline='black')
    
    return img

    