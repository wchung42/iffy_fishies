'''
#TeamSeas

 - Generate Tangram Fish with PIL; 1 of 3 designs
 - Scale and transform based on donation and randomness
 - Make background transparent
 - Save image
 - Overlay onto main canvas

'''

from PIL import Image, ImageTk
from generate_fish import draw_fish_design_1, draw_fish_design_2, draw_fish_design_3, transform, calc_scale_multiplier
import tkinter as tk
from tkinter import filedialog
import random

FONT_NAME = 'Courier'
HEIGHT = 2160
WIDTH = 3840

main_canvas = Image.new(mode='RGBA', color='#000000', size=(WIDTH, HEIGHT))
gif_imgs = []

# ---------------------------- Iffy Fishy Functions ------------------------------- #
def create_fish():
    size_multiplier = calc_scale_multiplier(random.randrange(1, 751, 5))
    fish_funcs = [draw_fish_design_1(), draw_fish_design_2(), draw_fish_design_3()]
    chosen_fish_func = random.choice(fish_funcs) # choose random fish function
    original_img = chosen_fish_func # call chosen function

    # transform generated fish image
    rotation_range = (-45, 45)
    transformed_img = transform(original_img, rotation_range, size_multiplier)
    
    return original_img, transformed_img

def display_fish():
    global img_to_save

    original_fish_img, transformed_fish_img = create_fish()

    # save original image
    img_to_save = original_fish_img

    fish_img_width, fish_img_height = transformed_fish_img.size
    resized_fish_img = transformed_fish_img.resize((round(fish_img_width/1.5), round(fish_img_height/1.5)), Image.ANTIALIAS)

    fish = ImageTk.PhotoImage(resized_fish_img)

    # fish_label.config(image=fish)
    # fish_label.photo = fish # assign to class variable to fix photoimage bug

    # fish_label.grid(column=1, row=1)
    root.fish = fish # prevent the image garbage collected
    canvas.create_image(250, 250, image=fish, anchor='center')

def save_fish():
    if img_to_save is None:
        return

    filename = filedialog.asksaveasfile(mode='wb', title='Save file', defaultextension='.png', filetypes=(('PNG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))

    if not filename:
        return

    img_to_save.save(filename)

# ---------------------------- main ------------------------------- #

if __name__=='__main__':
    root = tk.Tk()
    root.title('Iffy Fishies')
    root.config(padx=50, pady=25)

    logo_img = Image.open('./images/teamseas-tm-logo.png')
    logo_width, logo_height = logo_img.size
    resized_logo = logo_img.resize((logo_width//2, logo_height//2), resample=Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(resized_logo)
    logo_label = tk.Label(image=logo)
    logo_label.grid(column=1, row=0)

    canvas = tk.Canvas(width=500, height=500)
    canvas.grid(column=1, row=1)
    # fish_label = tk.Label(canvas)
    # fish_label.grid(column)
    # fish_label.place(relx=0.5, rely=0.5, anchor='center')

    img_to_save = None
    
    fish_btn = tk.Button(root, text='Create Fish', font=(FONT_NAME, 13, 'normal'), command=display_fish)
    fish_btn.grid(column=0, row=2)

    save_btn = tk.Button(root, text='Save Fish', font=(FONT_NAME, 13, 'normal'), command=save_fish)
    save_btn.grid(column=2, row=2)

    root.mainloop()


# for i in range(50):
#     multiplier = calc_scale_multiplier(random.randrange(1, 751, 5))
    
#     fish_func = [draw_fish_design_1(multiplier), draw_fish_design_2(multiplier), draw_fish_design_3(multiplier)]
#     gen_fish_func = random.choice(fish_func)
#     img = gen_fish_func
#     #img.save(f'Fish/fish{i}.png')
#     coors = (random.randrange(25, 3500), random.randrange(25, 2050))
    
#     main_canvas.alpha_composite(img, dest=coors)
    
#     print(f'Fish {i} has been created.')
    
# main_canvas.save('test_main.png')
    
