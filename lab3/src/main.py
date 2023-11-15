import cv2
from PIL import Image as Img
from PIL import ImageTk as ImgTk
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror


def high_pass_filter(img, kernel):
    """
    Функция принимает изображение и возвращает результат применения фильтра повышения резкости.
    """
    # kernel = np.array([[0, -1, 0],
    #                    [-1, 5, -1],
    #                    [0, -1, 0]])
    return cv2.filter2D(img, -1, kernel)


def _compute_otsu_criteria(im, th):
    # create the thresholded image
    thresholded_im = np.zeros(im.shape)
    thresholded_im[im >= th] = 1

    # compute weights
    nb_pixels = im.size
    nb_pixels1 = np.count_nonzero(thresholded_im)
    weight1 = nb_pixels1 / nb_pixels
    weight0 = 1 - weight1

    # if one of the classes is empty, eg all pixels are below or above the threshold,
    # that threshold will not be considered in the search for the best threshold
    if weight1 == 0 or weight0 == 0:
        return np.inf

    # find all pixels belonging to each class
    val_pixels1 = im[thresholded_im == 1]
    val_pixels0 = im[thresholded_im == 0]

    # compute variance of these classes
    var1 = np.var(val_pixels1) if len(val_pixels1) > 0 else 0
    var0 = np.var(val_pixels0) if len(val_pixels0) > 0 else 0

    return weight0 * var0 + weight1 * var1


def otsu_thresholding(img: np.ndarray) -> np.ndarray:
    threshold_range = range(np.max(img)+1)
    criterias = np.array([_compute_otsu_criteria(img, th) for th in threshold_range])

    # best threshold is the one minimizing the Otsu criteria
    best_threshold = threshold_range[np.argmin(criterias)]

    binary = img
    binary[binary > best_threshold] = 255
    binary[binary <= best_threshold] = 0

    return binary


def global_thresholding_otsu(img):
    """
    Функция выполняет глобальную пороговую обработку для входного изображения. Она принимает изображение в качестве параметра.
    Она преобразует изображение в черно-белое, присваивая значениям пикселей, большим пороговому значению, значение 255 (белый)
    и значениям пикселей, меньшим пороговому значению, значение 0 (черный). Она использует метод Оцу для определения порогового
    значения.
    """
    return otsu_thresholding(img)


def global_thresholding(img):
    """
    Функция выполняет глобальную пороговую обработку для входного изображения. Она принимает изображение и порог в качестве
    параметров. Она преобразует изображение в черно-белое, присваивая значениям пикселей, большим пороговому значению, значение
    255 (белый) и значениям пикселей, меньшим пороговому значению, значение 0 (черный).
    """
    ret, result = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return result


def adaptive_thresholding(img):
    """
    Функция выполняет адаптивную пороговую обработку для входного изображения. Она принимает изображение в качестве параметра.
    Она преобразует изображение в черно-белое, выполняя адаптивную пороговую обработку с размером блока 11
    """
    result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return result


global filepath
filepath = ''


def get_image():
    global filepath
    filepath = filedialog.askopenfilename()
    if not filepath:
        return
    file_path.delete(0, END)
    file_path.insert(INSERT, filepath)
    image = Img.open(filepath)
    global photo
    photo = ImgTk.PhotoImage(image.resize((500, 500)))
    canvas.create_image(0, 0, anchor='nw', image=photo)


# Применение фильтров
def apply_filter():
    if filepath == '':
        showerror(title='Error', message='No file selected')
        return

    selected_filters = filter_listbox.curselection()
    if not selected_filters:
        showerror(title='Error', message='No filter selected')
        return

    selected_filter = filter_listbox.get(selected_filters[0])

    if selected_filter == 'Original':
        canvas.create_image(0, 0, anchor='nw', image=photo)
    else:
        img = cv2.imread(filepath)
        print(selected_filter)
        global final
        for cmp_filter, method in (
                ('Global Thresholding', global_thresholding),
                ('Global Thresholding Otsu', global_thresholding_otsu),
                ('Adaptive Thresholding', adaptive_thresholding),
        ):
            if selected_filter == cmp_filter:
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                new_img = method(gray_img)
                new_image = Img.fromarray(new_img)
                final = ImgTk.PhotoImage(new_image.resize((500, 500)))
                canvas.create_image(0, 0, anchor='nw', image=final)
                break
        else:
            if selected_filter == "High Pass Filter 1.9":
                kernel = np.array([[-1, -1, -1],
                                   [-1, 9, -1],
                                   [-1, -1, -1]])
                new_img = high_pass_filter(img, kernel)
                new_image = Img.fromarray(new_img)
                final = ImgTk.PhotoImage(new_image.resize((500, 500)))
                canvas.create_image(0, 0, anchor='nw', image=final)
            elif selected_filter == "High Pass Filter 2.5":
                kernel = np.array([[1, -2, 1],
                                   [-2, 5, -2],
                                   [1, -2, 1]])
                new_img = high_pass_filter(img, kernel)
                new_image = Img.fromarray(new_img)
                final = ImgTk.PhotoImage(new_image.resize((500, 500)))
                canvas.create_image(0, 0, anchor='nw', image=final)
            elif selected_filter == "High Pass Filter 1.5":
                kernel = np.array([[0, -1, 0],
                                   [-1, 5, -1],
                                   [0, -1, 0]])
                new_img = high_pass_filter(img, kernel)
                new_image = Img.fromarray(new_img)
                final = ImgTk.PhotoImage(new_image.resize((500, 500)))
                canvas.create_image(0, 0, anchor='nw', image=final)
            elif selected_filter == "High Pass Filter LoG":
                kernel = np.array([[0, 0, -1, 0, 0],
                                   [0, -1, -2, -1, 0],
                                   [-1, -2, 16, -2, -1],
                                   [0, -1, -2, -1, 0],
                                   [0, 0, -1, 0, 0]])
                new_img = high_pass_filter(img, kernel)
                new_image = Img.fromarray(new_img)
                final = ImgTk.PhotoImage(new_image.resize((500, 500)))
                canvas.create_image(0, 0, anchor='nw', image=final)


root = Tk()
root.title("Digital image processing")
root.geometry('800x600')

btn_file_path = Button(root, text="Browse", command=get_image, width=10)
btn_file_path.grid(row=0, column=0, padx=20, pady=20, sticky=EW)

file_path = Entry(root, width=70)
file_path.grid(row=0, column=1, padx=20, pady=20, sticky=EW)
file_path.insert(INSERT, "Select an image...")

menu_frame = Frame(root)
menu_frame.grid(row=1, column=0, padx=15, pady=30, sticky=NS)

filter_listbox = Listbox(menu_frame, selectmode=SINGLE)
filter_listbox.pack(padx=20)

filters = ["Original", "High Pass Filter 1.9", "High Pass Filter 2.5", "High Pass Filter 1.5",
           "High Pass Filter LoG", "Global Thresholding", "Global Thresholding Otsu", "Adaptive Thresholding"]
for filter_name in filters:
    filter_listbox.insert(END, filter_name)

apply_button = Button(menu_frame, text="Apply Filter", command=apply_filter, width=15)
apply_button.pack(pady=20)

style = ttk.Style()
style.theme_use("default")

root.grid_rowconfigure(1, weight=1)

root.grid_columnconfigure(1, weight=1)

canvas = Canvas(root, height=500, width=500)
canvas.grid(row=1, column=1)

root.resizable(False, False)
root.mainloop()
