from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from PIL import Image

supported_formats = 'jpg,gif,tif,bmp,png,pcx'.split(',')
default_path = 'test_files/check1'


def get_files(path=default_path):
    global supported_formats
    try:
        os.listdir(path)
    except FileNotFoundError:
        return []
    return [os.path.join(path, file)
            for file in os.listdir(path)
            if file.split('.')[-1] in supported_formats]


def get_image_info(file):
    image = Image.open(file)
    return {
        'filename': file.split('/')[-1],
        'size': image.size,
        'resolution': image.info.get('dpi'),
        'depth': image.mode,
        'compression': image.info.get('compression', 'N/A')
    }


# tkinter app: one frame with interface to select folder(with files), button to start processing
# and table with results
root = Tk()
root.title('Image info')
root.geometry('800x600')
root.maxsize(800, 600)

frame = Frame(root)
frame.pack(fill=BOTH, expand=True)

folder_path = StringVar()
folder_path.set(default_path)
table = ttk.Treeview(frame, columns=('filename', 'size', 'resolution', 'depth', 'compression'))
table['show'] = 'headings'
table.grid(row=1, column=0, columnspan=3, sticky=NSEW)
table.column('filename', width=160)
table.column('size', width=100)
table.column('resolution', width=100)
table.column('depth', width=30)
table.column('compression', width=50)
table.heading('filename', text='Filename')
table.heading('size', text='Size')
table.heading('resolution', text='Resolution')
table.heading('depth', text='Depth')
table.heading('compression', text='Compression')


def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_path.set(folder)


def process():
    table.delete(*table.get_children())
    files = get_files(folder_path.get())
    for file in files:
        info = get_image_info(file)
        table.insert('', 'end', values=(info['filename'], info['size'], info['resolution'],
                                        info['depth'], info['compression']))
    table.update()


folder_label = Label(frame, textvariable=folder_path)
folder_label.grid(row=0, column=0)
select_folder_button = Button(frame, text='Select folder', command=select_folder)
select_folder_button.grid(row=0, column=1)
process_button = Button(frame, text='Process', command=process)
process_button.grid(row=0, column=2)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)

root.mainloop()
