import tkinter as tk
from tkinter import Tk, Label, Button, TOP, LEFT, RIGHT
from PIL import ImageTk, Image
from PIL.ImageTk import PhotoImage


class Gui(object):
    '''Graphical User Interphase builder in tkinter'''
    def __init__(self, title='GUI', root_height=900, root_width=700):
        self.root = Tk()
        self.root.title = title
        self.root.geometry(f'{root_height}x{root_width}')
        self.crossed = self.create_image(
            30, 30, r"C:\Users\Uchek\Protocol\Sofia\Interactive_gui\assets\crossed.jpg")
        self.n_routines = 3
        self.selected_routines = [False for _ in range(self.n_routines)]

    def create_image(self, width, height, filename):
        image = Image.open(filename)
        resize_image = image.resize((width, height))
        img = PhotoImage(resize_image)
        return img

    # the only images within the guy are the boxes that are either ticked or not
    def add_image(self, task, image_to_add: PhotoImage, row, column, grid=True, padx=0, pady=0, side=TOP):
        if grid == True:
            my_img = Label(self.root, image=image_to_add)
            my_img.grid(row=row, column=column)
        else:
            my_img = Label(self.root, image=image_to_add)
            my_img.pack(side=side, padx=padx, pady=pady)
        if task == 'task0':
            self.ticked_box0 = my_img
        elif task == 'task1':
            self.ticked_box1 = my_img
        else:
            pass

    def add_entry(self, row, column):
        entry1 = tk.Entry(self.root).grid(
            row=row, column=column)
        self.entry1 = entry1

    def add_text(self, text, font_style, font_size, row, column, grid=True, padx=0, pady=0, side=TOP):
        if grid == True:
            Label(self.root, text=text, font=(font_style, font_size)).grid(
                row=row, column=column)
        else:
            Label(self.root, text=text, font=(font_style, font_size)).pack(
                side=side, padx=padx, pady=pady)

    def add_btn(self, text, func,  row, column, grid=True, padx=0, pady=0, side=TOP):
        if grid == True:
            Button(self.root, text=text, command=func).grid(
                row=row, column=column)
        else:
            Button(self.root, text=text, command=func).pack(
                side=side, padx=padx, pady=pady)

    def start(self):
        self.root.mainloop()

def custom_function():
    global entry1
    print("this is the system response",entry1)

if __name__ == "__main__":
    gui = Gui()
    gui.add_text('Describe what the session entails', 'Helvetica', 17, 6, 1)
    gui.add_entry(7, 1)
    entry1 = gui.entry1
    gui.add_btn("delete emails",custom_function,8,1)
    gui.start()
