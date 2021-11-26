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

def transform(image, rotate_range, size_multiplier=1):
    '''Rotates given image within rotate_range, flips image and returns the resulting image'''
    start, end =  rotate_range
    result = image.rotate(randrange(start, end))
    
    if randrange(0, 5) == 1:
        result = result.transpose(method=Image.FLIP_LEFT_RIGHT)
    
    result = result.resize((round(1000*size_multiplier), round(1000*size_multiplier)), resample=Image.ANTIALIAS)
        
    return result
    
def draw_fish_design_1(size):
    '''Generate fish with design #1'''
    
    img = Image.new('RGBA', (1000, 1000), (255, 0, 0, 0))

    draw = ImageDraw.Draw(img)
    
    draw.polygon([(450, 175), (450, 500), (150, 500)], fill=rand_color(), outline='black') #triangle 1 head
    draw.polygon([(450, 825), (450, 500), (150, 500)], fill=rand_color(), outline='black') #triangle 2 head
    draw.polygon([(450, 240), (450, 594), (625, 417)], fill=rand_color(), outline='black') # triangle 3 body
    draw.polygon([(450, 594), (625, 417), (625, 583), (450, 760)], fill=rand_color(), outline='black') # rhombus body
    draw.polygon([(625, 417), (791, 417), (791, 583), (625, 583)], fill=rand_color(), outline='black') # square body
    draw.polygon([(625, 417), (791, 417), (791, 251)], fill=rand_color(), outline='black') # triangle top fin
    draw.polygon([(625, 583), (791, 583), (791, 749)], fill=rand_color(), outline='black') # triangle bottom fin

    return transform(img, (0, 45), size)

# def draw_fish_design_2(size):
#     '''Generate fish with design #2'''
#     img = Image.new('RGBA', (1000, 1000), (255, 0, 0, 0))
    
#     draw = ImageDraw.Draw(img)
    
#     draw.polygon([(750, 500), (750, 666), rand_coor(850, 920, 600, 690), (916, 500)], fill=rand_color(), outline='black') # square head
#     draw.polygon([(750, 500), (916, 500), (750, 344)], fill=rand_color(), outline='black') #triangle head
#     draw.polygon([(750, 344), (750, 666), (473, 344)], fill=rand_color(), outline='black') #triangle body 1
#     draw.polygon([(472, 344), (231, 578), (675, 578)], fill=rand_color(), outline='black') # triangle body 2
#     draw.polygon([(231, 578), rand_coor(50, 90, 525, 580), rand_coor(200, 240, 710, 760)], fill=rand_color(), outline='black')
#     draw.polygon([(750, 344), rand_coor(650, 725, 250, 300), rand_coor(525, 575, 100, 280), rand_coor(550, 600, 290, 325)], fill=rand_color(), outline='black') # rhombus top fin (br, tr, tl, bl)
#     draw.polygon([(675, 578), rand_coor(600, 650, 625, 700), rand_coor(444, 525, 590, 650)], fill=rand_color(), outline='black') # triangle bottom fin

#     return transform(img, (0, 45), size)

def draw_fish_design_2(size):
    '''Generate fish with design #2'''
    img = Image.new('RGBA', (1000, 1000), (255, 0, 0, 0))
    
    draw = ImageDraw.Draw(img)
    
    square_top_left = rand_coor(725, 775, 475, 525)
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
    top_fin_bl = (head_triangle_top[0] - randrange(69, 139), head_triangle_top[1] - randrange(25, 75))
    top_fin_tl = (head_triangle_top[0] - randrange(75, 125), head_triangle_top[1] - randrange(100, 150))
    top_fin_tr = (head_triangle_top[0] - randrange(25, 45), head_triangle_top[1] - randrange(75, 125))
    draw.polygon([head_triangle_top, top_fin_bl, top_fin_tl, top_fin_tr], fill=rand_color(), outline='black')

    # tail - triangle with respect to body_triangleish_b_bottom_left
    tail_top = (body_triangleish_b_bottom_left[0] - randrange(35, 100), body_triangleish_b_bottom_left[1] - randrange(35, 100))
    tail_bottom = (body_triangleish_b_bottom_left[0] - randrange(35, 100), body_triangleish_b_bottom_left[1] + randrange(35, 100))
    draw.polygon([body_triangleish_b_bottom_left, tail_top, tail_bottom], fill=rand_color(), outline='black')

    return transform(img, (0, 90), size)

def draw_fish_design_3(size):
    '''Generate fish with design #3'''
    img = Image.new('RGBA', (1000, 1000), (255, 0, 0, 0))
    
    draw = ImageDraw.Draw(img)
    
    draw.polygon([(800, 500), (588, 288), (588, 712)], fill=rand_color(), outline='black') # triangle head 1
    draw.polygon([(588, 288), (588, 712), (376, 500)], fill=rand_color(), outline='black') # triangle head 2
    draw.polygon([(588, 712), (482, 818), (376, 712), (482, 606)], fill=rand_color(), outline='black') # bottom fin square
    draw.polygon([(482, 818), (376, 712), rand_coor(325, 400, 775, 875)], fill=rand_color(), outline='black') # bottom fin triangle
    draw.polygon([(588, 288), (482, 182), (482, 394)], fill=rand_color(), outline='black') # top fin triangle
    draw.polygon([(482, 182), (482, 394), (376, 288), rand_coor(370, 400, 80, 150)], fill=rand_color(), outline='black') # top fin rhombus
    draw.polygon([(376, 500), rand_coor(270, 325, 394, 425), rand_coor(270, 325, 550, 606)], fill=rand_color(), outline='black') # tail triangle
    
    return transform(img, (-45, 45),  size)

    