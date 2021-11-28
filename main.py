'''
#TeamSeas

 - Generate Tangram Fish with PIL; 1 of 3 designs
 - Scale and transform based on donation and randomness
 - Make background transparent
 - Save image
 - Overlay onto main canvas

'''

from PIL import Image, ImageTk
from generate_fish import *
import tkinter as tk
from tkinter import filedialog
import random

FONT_NAME = 'Courier'
HEIGHT = 2160
WIDTH = 3840

BG_COLOR = '#89CFF0'

main_canvas = Image.new(mode='RGBA', color=BG_COLOR, size=(WIDTH, HEIGHT))
gif_imgs = []

# ---------------------------- Iffy Fishy Functions ------------------------------- #
def create_fish():
    global orig_img_to_save
    global trans_img_to_save

    size_multiplier = calc_scale_multiplier(random.randrange(1, 751, 5))
    fish_funcs = [draw_fish_design_1(), draw_fish_design_2(), draw_fish_design_3()]
    chosen_fish_func = random.choice(fish_funcs) # choose random fish function
    original_fish_img = chosen_fish_func # call chosen function

    # transform generated fish image
    rotation_range = (-45, 45)
    transformed_fish_img = transform(original_fish_img, rotation_range)
    resized_transformed_fish_img = resize(transformed_fish_img, size_multiplier)

    # # add to global fish images list
    # fish_imgs.append((original_fish_img, resized_transformed_fish_img))

    # save original image and transformed image
    orig_img_to_save = original_fish_img
    trans_img_to_save = transformed_fish_img
    
    return resized_transformed_fish_img

def display_fish(fish):
    global orig_img_to_save
    global trans_img_to_save    

    # resize to fit 500x500 canvas
    fish_img_width, fish_img_height = fish.size
    resized_fish_img = fish.resize((round(fish_img_width/1.5), round(fish_img_height/1.5)), Image.ANTIALIAS)

    fish = ImageTk.PhotoImage(resized_fish_img)
    root.fish = fish # prevent the image garbage collected
    preview_canvas.create_image(250, 250, image=fish, anchor='center')

def create_and_display():
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

def ready_canvas_for_gif():
    '''Clears the canvas and sets dimensions for GIF'''
    global gif_image

    preview_canvas.delete('all')
    preview_canvas.config(width=960, height=540)
    gif_preview = gif_image.resize((960, 540), Image.ANTIALIAS)
    ph_gif_preview = ImageTk.PhotoImage(gif_preview)
    root.ph_gif_preview = ph_gif_preview
    preview_canvas.itemconfig(canvas_image, image=ph_gif_preview)

def create_gif(frames):
    '''Creates iffy fishy images and returns a GIF '''
    global frame_counter
    global gif_frames
    global gif_image

    gif_preview = gif_image.resize((960, 540), Image.ANTIALIAS)
    ph_gif_preview = ImageTk.PhotoImage(gif_preview)
    root.ph_gif_preview = ph_gif_preview
    canvas_image = preview_canvas.create_image(480, 270, image=ph_gif_preview, anchor='center')
    
    image = create_fish()

    cors = (random.randrange(25, 3500), random.randrange(25, 1900))
    gif_image.alpha_composite(image, dest=cors)
    gif_preview = gif_image.resize((960, 540), Image.ANTIALIAS)
    ph_gif_preview = ImageTk.PhotoImage(gif_preview)
    root.ph_gif_preview = ph_gif_preview

    preview_canvas.itemconfig(canvas_image, image=ph_gif_preview)

    gif_frames.append(gif_image.resize((1920, 1080), Image.ANTIALIAS))

    if frames > 1:
        root.after(25, create_gif, frames-1)

def create_50():
    ready_canvas_for_gif()
    create_gif(50)

def add_to_gif():
    try:
        num = num_fishies.get()
        create_gif(int(num))
        num_entry.delete(0, len(num))
    except ValueError:
        return

def save_gif():
    global gif_frames
    global gif_image

    filename = filedialog.asksaveasfile(mode='wb', title='Save file', initialfile='your_iffy_fishy_giffy', defaultextension='.gif', filetypes=[('GIF', '*.gif')])
    gif_frames[0].save(filename, save_all=True, append_images=gif_frames[1:], optimize=True, duration=125, loop=0)

    # reset gif_image
    gif_image = Image.new(mode='RGBA', color=BG_COLOR, size=(WIDTH, HEIGHT))

# ---------------------------- main ------------------------------- #

if __name__=='__main__':
    root = tk.Tk()
    root.title('Iffy Fishies')
    root.config(padx=50, pady=25)

    logo_img = Image.open('./images/logo.png')
    logo_width, logo_height = logo_img.size
    resized_logo = logo_img.resize((logo_width//2, logo_height//2), resample=Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(resized_logo)
    logo_label = tk.Label(image=logo)
    logo_label.grid(column=0, row=0)

    # Initialize preview canvas with default screen
    preview_canvas = tk.Canvas(width=500, height=500)
    preview_canvas.grid(column=0, row=1)
    default_preview = ImageTk.PhotoImage(Image.new(mode='RGBA', color=BG_COLOR, size=(500, 500)))
    canvas_image = preview_canvas.create_image(250, 250, image=default_preview, anchor='center')
    
    orig_img_to_save = None
    trans_img_to_save = None

    fish_imgs = [] # (orig, trans)

    # GIF variables
    gif_frames = []

    gif_image = Image.new(mode='RGBA', color=BG_COLOR, size=(WIDTH, HEIGHT))

    # Button frame
    button_frame = tk.Frame(root)
    button_frame.grid(column=0, row=2)
    
    # Image button frame
    img_button_frame = tk.Frame(button_frame)
    img_button_frame.grid(column=0, row=0, padx=(0, 75))

    fish_btn = tk.Button(img_button_frame, text='Create Fish', font=(FONT_NAME, 11, 'normal'), command=create_and_display)
    fish_btn.grid(column=0, row=1, padx=5, pady=5, sticky='nesw')

    save_orig_btn = tk.Button(img_button_frame, text='Save Original Fish', font=(FONT_NAME, 11, 'normal'), command=save_orig_fish)
    save_orig_btn.grid(column=0, row=2, padx=5, pady=5, sticky='nesw')

    save_trans_btn = tk.Button(img_button_frame, text='Save Transformed Fish', font=(FONT_NAME, 11, 'normal'), command=save_trans_fish)
    save_trans_btn.grid(column=0, row=3, padx=5, pady=5, sticky='nesw')

    # Gif button frame
    gif_button_frame  = tk.Frame(button_frame)
    gif_button_frame.grid(column=1, row=0)

    gif_create_50_btn = tk.Button(gif_button_frame, text='Create 50', font=(FONT_NAME, 11, 'normal'), command=create_50)
    gif_create_50_btn.grid(column=0, row=0, padx=5, pady=5, sticky='nesw')

    # Gif add frame
    gif_add_frame = tk.Frame(gif_button_frame)
    gif_add_frame.grid(column=0, row=1)

    gif_add_btn = tk.Button(gif_add_frame, text='Add', font=(FONT_NAME, 11, 'normal'), command=add_to_gif)
    gif_add_btn.grid(column=0, row=0, padx=5, pady=5, sticky='nesw')

    num_fishies = tk.StringVar()
    num_entry = tk.Entry(gif_add_frame, textvariable=num_fishies, bd=5)
    num_entry.grid(column=1, row=0, sticky='nesw')

    save_fishtopia_btn = tk.Button(gif_button_frame, text='Save Fishtopia', font=(FONT_NAME, 11, 'normal'), command=None)
    save_fishtopia_btn.grid(column=0, row=2, padx=5, pady=5, sticky='nesw')

    gif_save_btn = tk.Button(gif_button_frame, text='Save GIF', font=(FONT_NAME, 11, 'normal'), command=save_gif)
    gif_save_btn.grid(column=0, row=3, padx=5, pady=5, sticky='nesw')

    root.mainloop()



    
