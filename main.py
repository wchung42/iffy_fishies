'''
IffyFishies
 - Coding 30 million fish for #TeamSeas

'''

from PIL import Image, ImageTk
from generate_fish import *
import tkinter as tk
from tkinter import filedialog
from tkinter.colorchooser import askcolor
import random
import requests

FONT_NAME = 'Helvetica'
HEIGHT = 2160
WIDTH = 3840

# ---------------------------- Iffy Fishy Functions ------------------------------- #
def create_fish(*args):
    global default_img
    global default_img_transformed
    global default_img_resized

    size_multiplier = None
    if len(args) != 0:
        size_multiplier = calc_scale_multiplier(int(args[0]))
    else:
        size_multiplier = calc_scale_multiplier(random.randrange(100, 751, 5))

    fish_funcs = [draw_fish_design_1(), draw_fish_design_2(), draw_fish_design_3()]
    chosen_fish_func = random.choice(fish_funcs) # choose random fish function
    original_fish_img = chosen_fish_func # call chosen function

    # transform generated fish image
    rotation_range = (-45, 45)
    transformed_fish_img = transform(original_fish_img, rotation_range)
    resized_transformed_fish_img = resize(transformed_fish_img, size_multiplier)

    default_img = original_fish_img
    default_img_transformed = transformed_fish_img
    default_img_resized = resized_transformed_fish_img

    return resized_transformed_fish_img


def display_fish(fish):
    '''Resized preview canvas and displays fish'''
    # resize canvas for single fish

    # resize to fit 500x500 canvas
    fish_img_width, fish_img_height = fish.size
    resized_fish_img = fish.resize((round(fish_img_width/1.5), round(fish_img_height/1.5)), Image.ANTIALIAS)

    fish = ImageTk.PhotoImage(resized_fish_img)
    root.fish = fish # prevent the image garbage collected
    preview_canvas.itemconfig(canvas_image, image=fish)


def create_and_display():
    '''Driver function for creating and displaying fish'''
    global canvas_image
    global default_img_resized

    # Enable image buttons
    save_orig_button.config(state=tk.NORMAL)
    save_transformed_button.config(state=tk.NORMAL)
    save_resized_button.config(state=tk.NORMAL)

    # preview_canvas.delete('all')
    # preview_canvas.config(width=500, height=500)
    # canvas_image = preview_canvas.create_image(250, 250, image=None, anchor='center')

    create_fish()
    display_fish(default_img_resized)


def save_orig_fish():
    if default_img is None:
        return

    filename = filedialog.asksaveasfile(mode='wb', title='Save file', initialfile='your_iffy_fishy_original', defaultextension='.png', filetypes=(('PNG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))
    if not filename:
        return

    color = preview_canvas.cget('bg') if preview_canvas.cget('bg') != 'SystemButtonFace' else None
    if color is None:
        default_img.save(filename)
    else:
        width, height = default_img.size
        background = Image.new('RGBA', (width, height), color=color)
        Image.alpha_composite(background, default_img).save(filename)
        
    
def save_trans_fish():
    if default_img_transformed is None:
        return

    filename = filedialog.asksaveasfile(mode='wb', title='Save file', initialfile='your_iffy_fishy_transformed', defaultextension='.png', filetypes=(('PNG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))
    if not filename:
        return

    color = preview_canvas.cget('bg') if preview_canvas.cget('bg') != 'SystemButtonFace' else None
    if color is None:
        default_img_transformed.save(filename)
    else:
        width, height = default_img_transformed.size
        background = Image.new('RGBA', (width, height), color=color)
        Image.alpha_composite(background, default_img_transformed).save(filename)


def save_resized_fish():
    if default_img_resized is None:
        return
    
    filename = filedialog.asksaveasfile(mode='wb', title='Save file', initialfile='your_iffy_fishy_resized', defaultextension='.png', filetypes=(('PNG', ('*.jpg','*.jpeg','*.jpe','*.jfif')),('PNG', '*.png'),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))
    if not filename:
        return

    color = preview_canvas.cget('bg') if preview_canvas.cget('bg') != 'SystemButtonFace' else None
    if color is None:
        default_img_resized.save(filename)
    else:
        width, height = default_img_resized.size
        background = Image.new('RGBA', (width, height), color=color)
        Image.alpha_composite(background, default_img_resized).save(filename)


def create_fishtopia(**kwargs):
    '''Create fishtopia collage with amount of fish, default = 50'''
    global fishtopia_collage

    # Enable collage buttons
    collage_add_button.config(state=tk.NORMAL)
    collage_save_button.config(state=tk.NORMAL)

    fishtopia_collage = Image.new('RGBA', (WIDTH, HEIGHT), color=None)

    if 'amount' in kwargs:
        try:
            amount = int(kwargs['amount'])
        except ValueError:
            pass
    else:
        amount = 50

    for _ in range(amount):
        fish = create_fish()
        
        cors = (random.randrange(0, 3700), random.randrange(0, 2000))
        fishtopia_collage.alpha_composite(fish, dest=cors)


def display_collage():
    '''Displays the fishtopia collage on screen'''
    # preview_canvas.delete('all')
    # preview_canvas.config(width=960, height=540)
    # canvas_image = preview_canvas.create_image(0, 0, image=None, anchor='nw')

    resized_fishtopia_collage = fishtopia_collage.resize((960, 540))
    preview = ImageTk.PhotoImage(resized_fishtopia_collage, Image.ANTIALIAS)
    root.preview = preview # save image data to local variable to bypass bug with photoimage
    preview_canvas.itemconfig(canvas_image, image=preview)


def create_collage():
    '''Driver function for create_fishtopia'''
    # global canvas_image
    try:
        num_fishies = int(starting_fishies.get())
        create_fishtopia(amount=num_fishies)
    except ValueError:
        create_fishtopia()
    finally:
        starting_fishies_entry.delete(0, tk.END)

    display_collage()

    
def add_to_fishtopia():
    '''Adds specified number of fish to fishtopia collage'''
    global fishtopia_collage
    global default_fishtopia_collage

    try:
        num_fishies = int(num_fishies_to_add.get())
    except ValueError:
        add_fishies_entry.delete(0, tk.END)
        return
    
    for _ in range(num_fishies):
        fish = create_fish()

        cors = (random.randrange(25, 3500), random.randrange(25, 1900))
        fishtopia_collage.alpha_composite(fish, dest=cors)

    display_collage()

    add_fishies_entry.delete(0, tk.END)


def save_fishtopia():
    '''Saves final canvas as an image'''
    if fishtopia_collage is None:
        return

    filename = filedialog.asksaveasfile(mode='wb', title='Save file', initialfile='your_iffy_fishy_fishtopia', defaultextension='.gif', filetypes=(('PNG', ('PNG', '*.png')),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))
    if not filename:
        return

    color = preview_canvas.cget('bg') if preview_canvas.cget('bg') != 'SystemButtonFace' else None
    if color is None:
        image_to_save = fishtopia_collage
    else:
        width, height = fishtopia_collage.size
        background = Image.new('RGBA', (width, height), color=color)
        image_to_save = Image.alpha_composite(background, fishtopia_collage)

    image_to_save.save(filename)

# ----------------------------- CHANGE BACKGROUND -------------------------------- #

def update_preview(color):
    if color is None:
        color = root.cget('bg')

    preview_canvas.config(bg=color)


def change_bg_transparent():
    color = None
    update_preview(color)


def change_bg_white():
    color = '#FFFFFF'
    update_preview(color)


def change_bg_blue():
    color = '#89CFF0'
    update_preview(color)


def change_bg_black():
    color = '#000000'
    update_preview(color)


def choose_color():
    color = askcolor(title='Choose color')
    return color


def change_bg_custom():
    color = choose_color()[1]
    if color is None:
        return
    update_preview(color)
    custom_color_button.config(bg=color)

# ------------------------------------- LIVE ------------------------------------ #
def update_live_counter():
    global live_count

    # get total amount donated
    resp = requests.get(url='https://tscache.com/donation_total.json')
    resp.raise_for_status()
    live_count = int(resp.json()['count'])

    live_count_label.config(text=live_count)

    root.after(10000, update_live_counter)


def create_live():
    global current_donations
    global live_image
    global live_count

    live_image = Image.new('RGBA', (WIDTH, HEIGHT), color=None)

    try:
        total_donated = int(live_count)
    except TypeError:
        print('Invalid type.')
    else:
        live_count_label.config(text=live_count)
        # populate image
        print('Populating the sea...')

        for _ in range(0, total_donated, 2000000):
            fish = create_fish(100)
            coors = (random.randrange(25, 3500), random.randrange(25, 1900))
            live_image.alpha_composite(fish, dest=coors)

    # get donation
    resp = requests.get(url='https://tscache.com/lb_recent.json')
    resp.raise_for_status()
    current_donations = resp.json()['recent'][:10]
   
    update_live_image()
        

def update_live_image():
    global current_donations
    global live_image
        
    # get donation
    resp = requests.get(url='https://tscache.com/lb_recent.json')
    resp.raise_for_status()
    new_donations = resp.json()['recent'][:10]

    new_fish_to_add_sizes = [data['pounds'] for data in new_donations if data not in current_donations]

    if len(new_fish_to_add_sizes) != 0:
        for fish_size in new_fish_to_add_sizes:
            fish = create_fish(fish_size)
            cors = (random.randrange(25, 3500), random.randrange(25, 1900))
            live_image.alpha_composite(fish, dest=cors)

        print('Congrats, you have spawned new iffy fishies!')
    
    current_donations = new_donations
    
    # show on canvas
    resized_live_image = live_image.resize((960, 540))
    preview = ImageTk.PhotoImage(resized_live_image, Image.ANTIALIAS)
    root.preview = preview # save image data to local variable to bypass bug with photoimage and gc
    preview_canvas.itemconfig(canvas_image, image=preview)

    # update every 30 seconds
    tk.after_id = root.after(30000, update_live_image)


def live_driver():
    change_mode()
    create_live()


def stop_live():
    try:
        root.after_cancel(tk.after_id)
    except AttributeError:
        pass
    except ValueError:
        pass
    else:
        print('Live mode stopped.')
        tk.after_id = None
        return


def save_live_image():
    '''Saves live image'''
    if live_image is None:
        return

    filename = filedialog.asksaveasfile(mode='wb', title='Save file', initialfile='your_iffy_fishy_aquarium', defaultextension='.gif', filetypes=(('PNG', ('PNG', '*.png')),('BMP', ('*.bmp','*.jdib')),('GIF', '*.gif')))
    if not filename:
        return

    color = preview_canvas.cget('bg') if preview_canvas.cget('bg') != 'SystemButtonFace' else None
    if color is None:
        image_to_save = live_image
    else:
        width, height = live_image.size
        background = Image.new('RGBA', (width, height), color=color)
        image_to_save = Image.alpha_composite(background, live_image)

    image_to_save.save(filename)

# ----------------------------- WINDOW MODE FUNCTIONS---------------------------- #
def change_mode():
    global canvas_image

    current_mode = mode.get()

    if current_mode == 'image':
        stop_live()
        print('Initializing image mode...')
        collage_buttons_frame.grid_remove()
        live_image_save_button.grid_remove()
        img_button_frame.grid()
    elif current_mode == 'collage':
        stop_live()
        print('Initializing collage mode...')
        img_button_frame.grid_remove()
        live_image_save_button.grid_remove()
        collage_buttons_frame.grid(column=0, row=2, sticky='ew')
        collage_buttons_frame.rowconfigure(0, weight=1)
        collage_buttons_frame.columnconfigure(0, weight=1)
    else:
        print('Initializing live mode...')
        img_button_frame.grid_remove()
        collage_buttons_frame.grid_remove()
        live_image_save_button.grid(column=0, row=2, sticky='ew')

    default_image = Image.new('RGBA', (960, 540), color=None)
    default_screen = ImageTk.PhotoImage(default_image, Image.ANTIALIAS)
    preview_canvas.itemconfig(canvas_image, image=default_screen)

# ----------------------------------- MAIN -------------------------------------- #

if __name__=='__main__':
    # Global variables
    default_img = None
    default_img_transformed = None
    default_img_resized = None
    default_fishtopia_collage = None
    fishtopia_collage = None
    live_image = None
    live_count = 0
    current_donations = []

    root = tk.Tk()
    root.title('Iffy Fishies')
    root.config(padx=20, pady=25)

    # Logos
    logo_frame = tk.Frame(root)
    logo_frame.grid(column=0, row=0, columnspan=2, pady=(0, 15))

    logo = Image.open('./images/logo.png')
    logo_width, logo_height = logo.size
    logo_pi = ImageTk.PhotoImage(logo.resize((round(logo_width/2), round(logo_height/2)), resample=Image.ANTIALIAS))
    logo_label = tk.Label(logo_frame, image=logo_pi)
    logo_label.grid(column=0, row=0)

    teamseas_logo = Image.open('./images/teamseas-logo.png')
    teamseas_logo_width, teamseas_logo_height = teamseas_logo.size
    teamseas_logo_pi = ImageTk.PhotoImage(teamseas_logo.resize((round(logo_width/2.5), round(logo_height/2.5)), resample=Image.ANTIALIAS))
    teamseas_logo_label = tk.Label(logo_frame, image=teamseas_logo_pi)
    teamseas_logo_label.grid(column=1, row=0)

    # ---------------------------------- LIVE COUNTER -------------------------------------#
    live_count_label = tk.Label(root, text=live_count, font=(FONT_NAME, 25, 'bold'))
    live_count_label.grid(column=0, row=1, pady=5, columnspan=2)
    update_live_counter()

    # ---------------------------------- PREVIEW SCREEN -------------------------------------#
    preview_canvas = tk.Canvas(width=960, height=540, bd=2, highlightthickness=1, highlightbackground='black')
    preview_canvas.grid(column=1, row=2)
    canvas_image = preview_canvas.create_image(480, 270, image=None, anchor='center')
    
    # ---------------------------------- CONTROL PANEL -------------------------------------#
    control_panel_frame = tk.Frame(root)
    control_panel_frame.grid(column=0, row=2, padx=(0, 10), sticky='n')
    control_panel_frame.grid_rowconfigure(0, weight=1)
    control_panel_frame.grid_columnconfigure(0, weight=1)

    # MODE SELECT CONTROLS
    mode_frame = tk.Frame(control_panel_frame, pady=5)
    mode_frame.grid(column=0, row=0)

    mode = tk.StringVar(value='image')
    image_mode = tk.Radiobutton(mode_frame, text='Image', value='image', variable=mode, indicatoron=False, bd=3, width=6, command=change_mode)
    image_mode.grid(column=0, row=0, padx=1)

    collage_mode = tk.Radiobutton(mode_frame, text='Collage', value='collage', variable=mode, indicatoron=False, bd=3, width=6, command=change_mode)
    collage_mode.grid(column=1, row=0, padx=1)

    live_mode = tk.Radiobutton(mode_frame, text='Live', value='live', variable=mode, indicatoron=False, bd=3, width=6, command=live_driver)
    live_mode.grid(column=2, row=0, padx=1)

    # BACKGROUND COLOR CONTROLS
    bg_color_buttons_frame = tk.Frame(control_panel_frame)
    bg_color_buttons_frame.grid(column=0, row=1, pady=5)

    transparent_button = tk.Button(bg_color_buttons_frame, text=' X ', bd=3, command=change_bg_transparent)
    transparent_button.grid(column=0, row=0, padx=5, pady=5, sticky='nesw')

    white_button = tk.Button(bg_color_buttons_frame, text='   ', bg='#FFFFFF', bd=3, command=change_bg_white)
    white_button.grid(column=1, row=0, padx=5, pady=5, sticky='nesw')

    blue_button = tk.Button(bg_color_buttons_frame, text='   ', bg='#89CFF0', bd=3, command=change_bg_blue)
    blue_button.grid(column=2, row=0,  padx=5, pady=5, sticky='nesw')

    black_button = tk.Button(bg_color_buttons_frame, text='   ', bg='#000000', bd=3, command=change_bg_black)
    black_button.grid(column=3, row=0,  padx=5, pady=5, sticky='nesw')

    custom_color_button = tk.Button(bg_color_buttons_frame, text='RGB', bd=3, command=change_bg_custom)
    custom_color_button.grid(column=4, row=0,  padx=5, pady=5, sticky='nesw')
    
    # Frame for single fish image related functions
    img_button_frame = tk.Frame(control_panel_frame)
    img_button_frame.grid(column=0, row=2, sticky='ew')
    img_button_frame.grid_rowconfigure(0, weight=1)
    img_button_frame.grid_columnconfigure(0, weight=1)

    fish_button = tk.Button(img_button_frame, text='Create Fish', bd=3, font=(FONT_NAME, 10, 'normal'), command=create_and_display)
    fish_button.grid(column=0, row=0, pady=5, sticky='ew')

    save_orig_button = tk.Button(img_button_frame, text='Save Original', bd=3, font=(FONT_NAME, 10, 'normal'), command=save_orig_fish, state=tk.DISABLED)
    save_orig_button.grid(column=0, row=1, pady=5, sticky='ew')

    save_transformed_button = tk.Button(img_button_frame, text='Save Transformed', bd=3, font=(FONT_NAME, 10, 'normal'), command=save_trans_fish, state=tk.DISABLED)
    save_transformed_button.grid(column=0, row=2, pady=5, sticky='ew')

    save_resized_button = tk.Button(img_button_frame, text='Save Resized', bd=3, font=(FONT_NAME, 10, 'normal'), command=save_resized_fish, state=tk.DISABLED)
    save_resized_button.grid(column=0, row=3, pady=5, sticky='ew')

    # Frame for Fishtopia Collage buttons
    collage_buttons_frame = tk.Frame(control_panel_frame)

    # Create collage frame
    collage_create_buttons_frame = tk.Frame(collage_buttons_frame)
    collage_create_buttons_frame.grid(column=0, row=1, sticky='ew')
    collage_create_buttons_frame.grid_rowconfigure(0, weight=1)
    collage_create_buttons_frame.grid_columnconfigure(0, weight=1)

    collage_create_btn = tk.Button(collage_create_buttons_frame, text='Create Fishtopia', bd=3, font=(FONT_NAME, 10, 'normal'), command=create_collage)
    collage_create_btn.grid(column=0, row=1, padx=5, pady=5, sticky='ew')

    starting_fishies = tk.StringVar()
    starting_fishies_entry = tk.Entry(collage_create_buttons_frame, textvariable=starting_fishies, bd=3, width=3)
    starting_fishies_entry.grid(column=1, row=1, sticky='ew')

    # Add fishies frame
    collage_add_button_frame = tk.Frame(collage_buttons_frame)
    collage_add_button_frame.grid(column=0, row=2, sticky='ew')
    collage_add_button_frame.grid_rowconfigure(0, weight=1)
    collage_add_button_frame.grid_columnconfigure(0, weight=1)

    collage_add_button = tk.Button(collage_add_button_frame, text='Add Fishies', bd=3, font=(FONT_NAME, 10, 'normal'), command=add_to_fishtopia, state=tk.DISABLED)
    collage_add_button.grid(column=0, row=0, padx=5, pady=5, sticky='nesw')

    num_fishies_to_add = tk.StringVar()
    add_fishies_entry = tk.Entry(collage_add_button_frame, textvariable=num_fishies_to_add, bd=3, width=9)
    add_fishies_entry.grid(column=1, row=0, sticky='ew')

    collage_save_button = tk.Button(collage_buttons_frame, text='Save Fishtopia', bd=3, font=(FONT_NAME, 10, 'normal'), command=save_fishtopia, state=tk.DISABLED)
    collage_save_button.grid(column=0, row=3, padx=5, pady=5, sticky='nesw')

    # SAVE LIVE IMAGE BUTTON
    live_image_save_button = tk.Button(control_panel_frame, text='Save Image', bd=3, font=(FONT_NAME, 10, 'normal'), command=save_live_image)

    root.mainloop()