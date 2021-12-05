'''
#TeamSeas

 - Generate Tangram Fish with PIL; 1 of 3 designs
 - Scale and transform based on donation and randomness
 - Make background transparent
 - Save image
 - Overlay onto main canvas

'''

from PIL import Image, ImageTk, ImageChops
from generate_fish import *
import tkinter as tk
from tkinter import filedialog
import random

FONT_NAME = 'Courier'
HEIGHT = 2160
WIDTH = 3840

# main_canvas = Image.new(mode='RGBA', color=BG_COLOR, size=(WIDTH, HEIGHT))

# ---------------------------- Iffy Fishy Functions ------------------------------- #
def create_fish():
    global default_img
    global default_img_transformed
    global default_img_resized
    global orig_img_to_save
    global trans_img_to_save
    global resized_img_to_save

    size_multiplier = calc_scale_multiplier(random.randrange(1, 751, 5))
    fish_funcs = [draw_fish_design_1(), draw_fish_design_2(), draw_fish_design_3()]
    chosen_fish_func = random.choice(fish_funcs) # choose random fish function
    original_fish_img = chosen_fish_func # call chosen function

    # transform generated fish image
    rotation_range = (-45, 45)
    transformed_fish_img = transform(original_fish_img, rotation_range)
    resized_transformed_fish_img = resize(transformed_fish_img, size_multiplier)

    # save original image and transformed image
    orig_img_to_save = original_fish_img
    trans_img_to_save = transformed_fish_img
    resized_img_to_save = resized_transformed_fish_img

    default_img = original_fish_img
    default_img_transformed = transformed_fish_img
    default_img_resized = resized_transformed_fish_img
    
    return resized_transformed_fish_img


def display_fish(fish):
    '''Resized preview canvas and displays fish'''
    # resize canvas for single fish
    preview_canvas.config(width=500, height=500)

    # resize to fit 500x500 canvas
    fish_img_width, fish_img_height = fish.size
    resized_fish_img = fish.resize((round(fish_img_width/1.5), round(fish_img_height/1.5)), Image.ANTIALIAS)

    fish = ImageTk.PhotoImage(resized_fish_img)
    root.fish = fish # prevent the image garbage collected
    preview_canvas.itemconfig(canvas_image, image=fish)


def create_and_display():
    '''Driver function for creating and displaying fish'''
    global canvas_image
    global mode

    mode = 'image'

    # Enable image buttons; Disable collage buttons
    save_orig_btn.config(state=tk.NORMAL)
    save_trans_btn.config(state=tk.NORMAL)
    save_resized_btn.config(state=tk.NORMAL)
    collage_add_btn.config(state=tk.DISABLED)
    collage_save_btn.config(state=tk.DISABLED)

    preview_canvas.delete('all')
    preview_canvas.config(width=500, height=500)
    canvas_image = preview_canvas.create_image(250, 250, image=None, anchor='center')

    fish = create_fish()
    display_fish(fish)


def save_orig_fish():
    if orig_img_to_save is None:
        return

    filename = filedialog.asksaveasfile(mode='wb', title='Save file', initialfile='your_iffy_fishy_original', defaultextension='.png', filetypes=(('PNG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))

    if not filename:
        return

    orig_img_to_save.save(filename)


def save_trans_fish():
    if trans_img_to_save is None:
        return

    filename = filedialog.asksaveasfile(mode='wb', title='Save file', initialfile='your_iffy_fishy_transformed', defaultextension='.png', filetypes=(('PNG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))

    if not filename:
        return

    trans_img_to_save.save(filename)


def save_resized_fish():
    if resized_img_to_save is None:
        return
    
    filename = filedialog.asksaveasfile(mode='wb', title='Save file', initialfile='your_iffy_fishy_resized', defaultextension='.png', filetypes=(('PNG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))

    if not filename:
        return

    resized_img_to_save.save(filename)


def create_fishtopia(**kwargs):
    '''Create fishtopia collage with amount of fish, default = 50'''
    global fishtopia_collage
    global default_fishtopia_collage
    global mode

    # Disable image buttons; Enable collage buttons
    save_orig_btn.config(state=tk.DISABLED)
    save_trans_btn.config(state=tk.DISABLED)
    save_resized_btn.config(state=tk.DISABLED)
    collage_add_btn.config(state=tk.NORMAL)
    collage_save_btn.config(state=tk.NORMAL)

    fishtopia_collage = Image.new('RGBA', (WIDTH, HEIGHT), color=(0, 0, 0, 0))

    if 'amount' in kwargs:
        try:
            amount = int(kwargs['amount'])
        except ValueError:
            pass
    else:
        amount = 50

    for _ in range(amount):
        fish = create_fish()
        
        cors = (random.randrange(5, 3700), random.randrange(5, 2000))
        fishtopia_collage.alpha_composite(fish, dest=cors)

    default_fishtopia_collage = fishtopia_collage

    resized_fishtopia_collage = fishtopia_collage.resize((960, 540))
    preview = ImageTk.PhotoImage(resized_fishtopia_collage, Image.ANTIALIAS)
    root.preview = preview # save image data to local variable to bypass bug with photoimage
    preview_canvas.itemconfig(canvas_image, image=preview)


def create_collage():
    '''Driver function for create_fishtopia'''
    global canvas_image
    global mode

    mode = 'collage'

    preview_canvas.delete('all')
    preview_canvas.config(width=960, height=540)
    canvas_image = preview_canvas.create_image(0, 0, image=None, anchor='nw')

    try:
        num_fishies = int(starting_fishies.get())
        create_fishtopia(amount=num_fishies)
    except ValueError:
        create_fishtopia()
    finally:
        starting_fishies_entry.delete(0, tk.END)
    

def add_to_fishtopia():
    '''Adds specified number of fish to fishtopia collage'''
    global fishtopia_collage

    try:
        num_fishies = int(num_fishies_to_add.get())
    except ValueError:
        return
    
    for _ in range(num_fishies):
        fish = create_fish()

        cors = (random.randrange(25, 3500), random.randrange(25, 1900))
        fishtopia_collage.alpha_composite(fish, dest=cors)

    preview = ImageTk.PhotoImage(fishtopia_collage.resize((960, 540), Image.ANTIALIAS))
    root.preview = preview # save image data to local variable to bypass bug with photoimage
    preview_canvas.itemconfig(canvas_image, image=preview)

    # clear entry text
    add_fishies_entry.delete(0, tk.END)


def save_fishtopia():
    '''Saves final canvas as an image'''
    global fishtopia_collage

    if fishtopia_collage is None:
        return

    filename = filedialog.asksaveasfile(mode='wb', title='Save file', initialfile='your_iffy_fishy_fishtopia', defaultextension='.gif', filetypes=(('PNG', ('PNG', '*.png')),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))

    if not filename:
        return

    fishtopia_collage.save(filename)


def update_preview(color):
    global default_img_resized
    global fishtopia_collage
    global mode

    if color is None:
        color = root.cget('bg')

    preview_canvas.config(bg=color)
    

def change_bg_color_single(color):
    '''Changes background color of image'''
    global default_img
    global default_img_transformed
    global default_img_resized
    global orig_img_to_save
    global trans_img_to_save
    global resized_img_to_save

    before_images = [default_img, default_img_transformed, default_img_resized]
    after_images = []

    if color is None:
        orig_img_to_save, trans_img_to_save, resized_img_to_save = before_images
        return

    for image in before_images:
        width, height = image.size
        new_bg = Image.new('RGBA', (width, height), color=color)
        
        image = Image.alpha_composite(new_bg, image)
        after_images.append(image)

    orig_img_to_save, trans_img_to_save, resized_img_to_save = after_images


def change_bg_color_collage(color):
    '''Changes background color of collage'''
    global default_fishtopia_collage
    global fishtopia_collage

    if color is None:
        fishtopia_collage = default_fishtopia_collage
        return

    width, height = fishtopia_collage.size
    new_bg = Image.new('RGBA', (width, height), color=color)
    fishtopia_collage = Image.alpha_composite(new_bg, default_fishtopia_collage)


def change_bg_transparent():
    global mode
    color = None
    if mode == 'image':
        change_bg_color_single(color)
    elif mode == 'collage':
        change_bg_color_collage(color)

    update_preview(color)


def change_bg_white():
    global mode
    color = '#FFFFFF'
    if mode == 'image':
        change_bg_color_single(color)
    elif mode == 'collage':
        change_bg_color_collage(color)
    
    update_preview(color)


def change_bg_blue():
    global mode
    color = '#89CFF0'
    if mode == 'image':
        change_bg_color_single(color)
    elif mode == 'collage':
        change_bg_color_collage(color)
   
    update_preview(color)


def change_bg_black():
    global mode
    color = '#000000'
    if mode == 'image':
        change_bg_color_single(color)
    elif mode == 'collage':
        change_bg_color_collage(color)

    update_preview(color)

# ---------------------------- main ------------------------------- #

if __name__=='__main__':
    # Global variables
    default_img = None
    default_img_transformed = None
    default_img_resized = None
    orig_img_to_save = None
    trans_img_to_save = None
    resized_img_to_save = None
    default_fishtopia_collage = None
    fishtopia_collage = None
    mode = 'image'

    root = tk.Tk()
    root.title('Iffy Fishies')
    root.config(padx=50, pady=25)

    logo_img = Image.open('./images/logo.png')
    logo_width, logo_height = logo_img.size
    logo = ImageTk.PhotoImage(logo_img.resize((round(logo_width/1.5), round(logo_height/1.5)), resample=Image.ANTIALIAS))
    logo_label = tk.Label(image=logo)
    logo_label.grid(column=0, row=0)

    # Initialize preview canvas with default screen
    preview_canvas = tk.Canvas(width=500, height=500)
    preview_canvas.grid(column=0, row=1)
    canvas_image = preview_canvas.create_image(250, 250, image=None, anchor='center')
    
    # Frame for button interface
    button_frame = tk.Frame(root)
    button_frame.grid(column=0, row=2)
    
    # Frame for single fish image related functions
    img_button_frame = tk.Frame(button_frame)
    img_button_frame.grid(column=0, row=0, padx=(0, 75))

    fish_btn = tk.Button(img_button_frame, text='Create Fish', font=(FONT_NAME, 11, 'normal'), command=create_and_display)
    fish_btn.grid(column=0, row=0, padx=5, pady=5, sticky='nesw')

    save_orig_btn = tk.Button(img_button_frame, text='Save Original', font=(FONT_NAME, 11, 'normal'), command=save_orig_fish, state=tk.DISABLED)
    save_orig_btn.grid(column=0, row=1, padx=5, pady=5, sticky='nesw')

    save_trans_btn = tk.Button(img_button_frame, text='Save Transformed', font=(FONT_NAME, 11, 'normal'), command=save_trans_fish, state=tk.DISABLED)
    save_trans_btn.grid(column=0, row=2, padx=5, pady=5, sticky='nesw')

    save_resized_btn = tk.Button(img_button_frame, text='Save Resized', font=(FONT_NAME, 11, 'normal'), command=save_resized_fish, state=tk.DISABLED)
    save_resized_btn.grid(column=0, row=3, padx=5, pady=5, sticky='nesw')

    # Frame for Fishtopia Collage buttons
    collage_btns_frame  = tk.Frame(button_frame)
    collage_btns_frame.grid(column=1, row=0)

    # Background color button frame
    bg_color_btns_frame = tk.Frame(collage_btns_frame)
    bg_color_btns_frame.grid(column=0, row=0)

    transparent_btn = tk.Button(bg_color_btns_frame, text=' X ', bd=3, command=change_bg_transparent)
    transparent_btn.grid(column=0, row=0, padx=10, pady=5, sticky='nesw')

    white_btn = tk.Button(bg_color_btns_frame, text='   ', bg='#FFFFFF', bd=3, command=change_bg_white)
    white_btn.grid(column=1, row=0, padx=10, pady=5, sticky='nesw')

    blue_btn = tk.Button(bg_color_btns_frame, text='   ', bg='#89CFF0', bd=3, command=change_bg_blue)
    blue_btn.grid(column=2, row=0,  padx=10, pady=5, sticky='nesw')

    black_btn = tk.Button(bg_color_btns_frame, text='   ', bg='#000000', bd=3, command=change_bg_black)
    black_btn.grid(column=3, row=0,  padx=10, pady=5, sticky='nesw')

    # Create fishtopia frame
    collage_create_btns_frame = tk.Frame(collage_btns_frame)
    collage_create_btns_frame.grid(column=0, row=1)

    collage_create_btn = tk.Button(collage_create_btns_frame, text='Create Fishtopia', font=(FONT_NAME, 11, 'normal'), command=create_collage)
    collage_create_btn.grid(column=0, row=1, padx=5, pady=5, sticky='nesw')

    starting_fishies = tk.StringVar()
    starting_fishies_entry = tk.Entry(collage_create_btns_frame, textvariable=starting_fishies, bd=5, width=4)
    starting_fishies_entry.grid(column=1, row=1, sticky='nesw')

    # Add fishies frame
    collage_add_btn_frame = tk.Frame(collage_btns_frame)
    collage_add_btn_frame.grid(column=0, row=2, sticky='nesw')

    collage_add_btn = tk.Button(collage_add_btn_frame, text='Add Fishies', font=(FONT_NAME, 11, 'normal'), command=add_to_fishtopia, state=tk.DISABLED)
    collage_add_btn.grid(column=0, row=0, padx=5, pady=5, sticky='nesw')

    num_fishies_to_add = tk.StringVar()
    add_fishies_entry = tk.Entry(collage_add_btn_frame, textvariable=num_fishies_to_add, bd=5, width=11)
    add_fishies_entry.grid(column=1, row=0, sticky='nesw')

    collage_save_btn = tk.Button(collage_btns_frame, text='Save Fishtopia', font=(FONT_NAME, 11, 'normal'), command=save_fishtopia, state=tk.DISABLED)
    collage_save_btn.grid(column=0, row=3, padx=5, pady=5, sticky='nesw')

    root.mainloop()