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

def rand_color():
    '''Returns a random RGB tuple'''
    
    return (randrange(0, 256), randrange(0, 256), randrange(0, 256), 255)

def rand_coor(x1, x2, y1, y2):
    '''Generates a random x and random y within given range and Returns a random (x,y) tuple'''
    
    return (randrange(x1, x2), (randrange(y1, y2)))

def transform(image, rotate_range, size=1):
    '''Rotates given image within rotate_range, flips image and returns the resulting image'''
    start, end =  rotate_range
    result = image.rotate(randrange(start, end))
    
    if randrange(0, 5) == 1:
        result = result.transpose(method=Image.FLIP_LEFT_RIGHT)
    
    result = result.resize((round(1000*size), round(1000*size)))
        
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

def draw_fish_design_2(size):
    '''Generate fish with design #2'''
    img = Image.new('RGBA', (1000, 1000), (255, 0, 0, 0))
    
    draw = ImageDraw.Draw(img)
    
    draw.polygon([(750, 500), (750, 666), rand_coor(850, 920, 600, 690), (916, 500)], fill=rand_color(), outline='black') # square head
    draw.polygon([(750, 500), (916, 500), (750, 344)], fill=rand_color(), outline='black') #triangle head
    draw.polygon([(750, 344), (750, 666), (473, 344)], fill=rand_color(), outline='black') #triangle body 1
    draw.polygon([(472, 344), (231, 578), (675, 578)], fill=rand_color(), outline='black') # triangle body 2
    #draw.polygon([(231, 578), (65, 578), (231, 744)], fill=rand_color()) # triangle tail
    draw.polygon([(231, 578), rand_coor(50, 90, 525, 580), rand_coor(200, 240, 710, 760)], fill=rand_color(), outline='black')
    draw.polygon([(750, 344), rand_coor(650, 725, 250, 300), rand_coor(525, 575, 100, 280), rand_coor(550, 600, 290, 325)], fill=rand_color(), outline='black') # rhombus top fin (br, tr, tl, bl)
    draw.polygon([(675, 578), rand_coor(600, 650, 625, 700), rand_coor(444, 525, 590, 650)], fill=rand_color(), outline='black') # triangle bottom fin

    return transform(img, (0, 45), size)

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

    