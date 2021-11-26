'''
#TeamSeas

 - Generate Tangram Fish with PIL; 1 of 5 designs
 - Scale and transform based on donation and randomness
 - Make background transparent
 - Save image
 - Overlay onto main canvas

'''
# Main canvas

from PIL import Image
from generate_fish import draw_fish_design_1, draw_fish_design_2, draw_fish_design_3
import random
import time

HEIGHT = 2160
WIDTH = 3840

main_canvas = Image.new(mode='RGBA', color='#000000', size=(WIDTH, HEIGHT))

def calc_scale_multiplier(val):
    '''Convert given val to a scaling multiplier'''
    if val >= 750:
        val = 750
    
    multiplier = val/1000
    
    if multiplier < 0.2:
        return 0.2
    else:
        return multiplier
    
for i in range(50):
    multiplier = calc_scale_multiplier(random.randrange(1, 751, 5))
    
    # fish_func = [draw_fish_design_1(multiplier), draw_fish_design_2(multiplier), draw_fish_design_3(multiplier)]
    #gen_fish_func = random.choice(fish_func)
    #img = gen_fish_func
    img = draw_fish_design_2(multiplier)
    #img.save(f'Fish/fish{i}.png')
    coors = (random.randrange(10, 3500), random.randrange(10, 2100))
    
    main_canvas.alpha_composite(img, dest=coors)
    
    print(f'Fish {i} has been created.')
    
main_canvas.save('test_main.png')
    
