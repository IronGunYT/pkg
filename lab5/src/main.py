import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter.messagebox import showerror
import re
import time


DEFAULT_FONT = ("Purisa", 8)


def round(x):
    # override round function
    if x >= 0:
        return int(x + 0.5)
    else:
        return int(x - 0.5)


class UiApp:
    dots = []  # unused
    raw_segments = []
    cutted_segments = []
    polygon = []
    cutted_polygon = []

    def __init__(self, master=None):
        # build ui
        frame1 = ttk.Frame(master)
        frame1.configure(height=600, width=800)
        frame3 = ttk.Frame(frame1)
        frame3.configure(height=200, width=200)
        label6 = ttk.Label(frame3)
        label6.configure(text='Координаты отсекающего окна')
        label6.pack(side="top")
        label1 = ttk.Label(frame3)
        label1.configure(text='x1')
        label1.pack(side="top")
        self.coord_x1 = ttk.Entry(frame3)
        self.coord_x1.configure(validate="all")
        self.coord_x1.pack(fill="x", pady=2, side="top")
        _validatecmd = (self.coord_x1.register(self.check_number), "%P")
        self.coord_x1.configure(validatecommand=_validatecmd)
        label2 = ttk.Label(frame3)
        label2.configure(text='y1')
        label2.pack(side="top")
        self.coord_y1 = ttk.Entry(frame3)
        self.coord_y1.configure(validate="all")
        self.coord_y1.pack(fill="x", pady=2, side="top")
        _validatecmd = (self.coord_y1.register(self.check_number), "%P")
        self.coord_y1.configure(validatecommand=_validatecmd)
        label3 = ttk.Label(frame3)
        label3.configure(text='x2')
        label3.pack(side="top")
        self.coord_x2 = ttk.Entry(frame3)
        self.coord_x2.configure(validate="all")
        self.coord_x2.pack(fill="x", pady=2, side="top")
        _validatecmd = (self.coord_x2.register(self.check_number), "%P")
        self.coord_x2.configure(validatecommand=_validatecmd)
        label4 = ttk.Label(frame3)
        label4.configure(text='y2')
        label4.pack(side="top")
        self.coord_y2 = ttk.Entry(frame3)
        self.coord_y2.configure(validate="all")
        self.coord_y2.pack(fill="x", pady=2, side="top")
        _validatecmd = (self.coord_y2.register(self.check_number), "%P")
        self.coord_y2.configure(validatecommand=_validatecmd)
        separator3 = ttk.Separator(frame3)
        separator3.configure(orient="horizontal")
        separator3.pack(pady=5, side="top")
        self.button_step = ttk.Button(frame3)
        self.button_step.configure(text='Выбрать файл...')
        self.button_step.pack(fill="x", pady=2, side="top")
        self.button_step.configure(command=self.load_segments)
        separator1 = ttk.Separator(frame3)
        separator1.configure(orient="horizontal")
        separator1.pack(pady=5, side="top")
        label5 = ttk.Label(frame3)
        label5.configure(text='Масштаб')
        label5.pack(side="top")
        self.scale_input = ttk.Spinbox(frame3, from_=2, to=100, command=self.update_all)
        self.scale_input.pack(side="top")
        frame3.pack(padx=12, pady=12, side="left")
        frame5 = ttk.Frame(frame1)
        frame5.configure(height=200, width=200)
        self.canvas = canvas3 = tk.Canvas(frame5)
        canvas3.configure(background="#FFFFFF")
        canvas3.pack(expand=True, fill="both", side="top")
        frame5.pack(expand=True, fill="both", padx=12, pady=12, side="right")
        frame1.pack(expand=True, fill="both", side="top")

        # Main widget
        self.mainwindow = frame1

        # initial
        self.mainwindow.config(height=600, width=1000)
        self.mainwindow.bind("<Configure>", self.update_all)
        self.scale = 12
        self.scale_input.set(self.scale)
        self.coord_x1.insert(0, '-2')
        self.coord_y1.insert(0, '-2')
        self.coord_x2.insert(0, '2')
        self.coord_y2.insert(0, '2')
        self.raw_segments = [
            [-5, 5, 2, -4],
            [-8, -8, 10, 11],
            [-2, -2, 3, 2],
            [1, 5, 1, -3],
            [0, -3, 4, -3],
        ]
        self.polygon = [
            [-1, -1],
            [0, 2],
            [3, 4],
            [5, 1],
            [3, -1],
        ]
        self.mainwindow.update()
        self.update_all()

    def run(self):
        self.mainwindow.mainloop()

    def show_alert(self):
        showerror("Ошибка", "Неверный формат ввода")

    def check_number(self, p_entry_value):
        # here check only allowed symbols without checking the value
        if not p_entry_value:
            return True
        if re.match(r'^[-0-9.,]*$', p_entry_value) is not None:
            return True
        return False

    def load_segments(self):
        filetypes = (
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )
        file = filedialog.askopenfilename(
            title='Выберите файл с исходными данными',
            filetypes=filetypes,
        )
        print(f'Opening file {file}')
        try:
            with open(file) as f:
                # читаем отрезки
                n = int(f.readline().strip())
                if n < 0:
                    raise Exception('n must be greater that zero')
                for _ in range(n):
                    x1, y1, x2, y2 = (float(i) for i in f.readline().strip())
                    self.raw_segments.append([x1, y1, x2, y2])
                # читаем многоугольник
                n = int(f.readline().strip())
                if n < 0:
                    raise Exception('n must be greater that zero')
                for _ in range(n):
                    x, y = (float(i) for i in f.readline().strip())
                    self.polygon.append([x, y])
        except Exception as e:
            showerror('Ошибка', f'Ошибка чтения файла: {e}')
        self.update_all()

    # region canvas util
    def update_scale(self, event=None):
        self.scale = int(self.scale_input.get())
        self.canvas.delete("all")  # Clear canvas
        self.draw_axes()
        self.draw_grid()

    def draw_axes(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Draw x-axis
        self.canvas.create_line(0, height / 2, width - 10, height / 2, arrow=tk.LAST)
        # Draw y-axis
        self.canvas.create_line(width / 2, height, width / 2, 10, arrow=tk.LAST)

    def draw_grid(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        x_spacing = width / (2 * self.scale)
        y_spacing = x_spacing

        # Draw x-axis gridlines
        for i in range(-self.scale, self.scale + 1):
            if i == 0:
                continue
            x = width / 2 + i * x_spacing
            self.canvas.create_line(x, 0, x, height, dash=(2, 2), fill="lightgray")
            # don't show first and last number because of arrows
            if i != self.scale and i != -self.scale:
                # if too big scale skip some numbers
                if 25 <= self.scale < 50:
                    if i % 2 == 0:
                        self.canvas.create_text(x, height / 2 + 4, text=str(i), anchor=tk.N, font=DEFAULT_FONT)
                elif self.scale >= 50:
                    if i % 5 == 0:
                        self.canvas.create_text(x, height / 2 + 4, text=str(i), anchor=tk.N, font=DEFAULT_FONT)
                else:
                    self.canvas.create_text(x, height / 2 + 4, text=str(i), anchor=tk.N, font=DEFAULT_FONT)

        # Draw y-axis gridlines (from bottom to top)
        # consider that the y-axis may be larger than the x-axis
        y_scale = int(height / (2 * y_spacing))
        for i in range(-y_scale, y_scale + 1):
            if i == 0:
                continue
            y = height / 2 + i * y_spacing
            self.canvas.create_line(0, y, width, y, dash=(2, 2), fill="lightgray")
            # don't show first and last number because of arrows
            if i != y_scale and i != -y_scale:
                # if too big scale skip some numbers
                if 25 <= self.scale < 50:
                    if i % 2 == 0:
                        self.canvas.create_text(width / 2 + 4, y, text=str(-i), anchor=tk.NW, font=DEFAULT_FONT)
                elif self.scale >= 50:
                    if i % 5 == 0:
                        self.canvas.create_text(width / 2 + 4, y, text=str(-i), anchor=tk.NW, font=DEFAULT_FONT)
                else:
                    self.canvas.create_text(width / 2 + 4, y, text=str(-i), anchor=tk.NW, font=DEFAULT_FONT)

        # draw zero
        self.canvas.create_text(width / 2 + 4, height / 2 + 4, text="0", anchor=tk.NW, font=DEFAULT_FONT)

    def get_real_coords(self, x, y):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        x_spacing = width / (2 * self.scale)
        y_spacing = x_spacing

        x = width / 2 + x * x_spacing
        y = height / 2 - y * y_spacing
        return x, y, x_spacing, y_spacing

    def draw_dot(self, x, y, color="red"):
        # fill one square of the grid with color
        x, y, x_spacing, y_spacing = self.get_real_coords(x, y)
        self.canvas.create_rectangle(x, y, x + x_spacing, y - y_spacing, fill=color)

    def draw_raw_line(self, x1, y1, x2, y2):
        x1, y1, _, _ = self.get_real_coords(x1, y1)
        x2, y2, _, _ = self.get_real_coords(x2, y2)
        self.canvas.create_line(x1, y1, x2, y2, dash=(4, 2), fill="gray", width=2)

    def draw_cutted_line(self, x1, y1, x2, y2):
        x1, y1, _, _ = self.get_real_coords(x1, y1)
        x2, y2, _, _ = self.get_real_coords(x2, y2)
        self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

    def update_dots(self):
        for dot in self.dots:
            self.draw_dot(dot[0], dot[1])

    def update_segments(self):
        for segm in self.raw_segments:
            self.draw_raw_line(*segm)
        for segm in self.cutted_segments:
            self.draw_cutted_line(*segm)

    def update_polygons(self):
        for polygon, func in (
                (self.polygon, self.draw_raw_line),
                (self.cutted_polygon, self.draw_cutted_line),
        ):
            if not polygon:
                continue
            c_x = polygon[0][0]
            c_y = polygon[0][1]
            for x, y in polygon[1:]:
                func(c_x, c_y, x, y)
                c_x = x
                c_y = y
            func(c_x, c_y, polygon[0][0], polygon[0][1])

    def update_all(self, event=None):
        for segm in self.raw_segments:
            self.cut_liang_barsky(*segm)
        self.canvas.delete("all")
        self.update_scale(event)
        self.draw_grid()
        self.draw_axes()
        self.update_dots()
        self.update_segments()
        self.update_polygons()
    # endregion

    def get_dots(self):
        try:
            arr = []
            for input_el in (self.coord_x1, self.coord_y1, self.coord_x2, self.coord_y2):
                arr.append(float(input_el.get().replace(',', '.')))
            if arr[0] == arr[2] and arr[1] == arr[3]:
                self.show_alert()
                return None
            return tuple(arr)
        except:
            self.show_alert()
            return None

    def cut_liang_barsky(self, s_x1, s_y1, s_x2, s_y2):
        self.dots = []
        start_dots = self.get_dots()
        if start_dots is None:
            return

        start_time = time.time()
        x1, y1, x2, y2 = start_dots  # отсекающее окно
        dx = x2 - x1
        dy = y2 - y1
        p = [-dx, dx, -dy, dy]
        q = [x1 - s_x1, s_x2 - x1, y1 - s_y1, s_y2 - y1]
        u1 = 0
        u2 = 1
        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return
            else:
                u = q[i] / p[i]
                if p[i] < 0:
                    u1 = max(u1, u)
                else:
                    u2 = min(u2, u)
        if u1 > u2:
            return
        x1 = x1 + u1 * dx
        y1 = y1 + u1 * dy
        x2 = x1 + u2 * dx
        y2 = y1 + u2 * dy
        self.cutted_segments.append([x1, y1, x2, y2])

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1000x600')
    root.title('Растеризация')
    root.minsize(600, 500)
    app = UiApp(root)
    app.run()
