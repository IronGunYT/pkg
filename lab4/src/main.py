import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
import re

"""
Написать приложение,иллюстрирующее работу базовых алгоритмов растеризации отрезков и кривых:
− пошаговый алгоритм;
− алгоритм ЦДА;
− алгоритм Брезенхема;
− алгоритм Брезенхема (окружность)

Интерфейс: ввод координат отрезка, 4 кнопки построения для разных алгоритмов и канвас для рисования
"""

DEFAULT_FONT = ("Purisa", 8)


def round(x):
    # override round function
    if x >= 0:
        return int(x + 0.5)
    else:
        return int(x - 0.5)


class UiApp:
    def __init__(self, master=None):
        # build ui
        frame1 = ttk.Frame(master)
        frame1.configure(height=600, width=800)
        frame3 = ttk.Frame(frame1)
        frame3.configure(height=200, width=200)
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
        label3.configure(text='x2/r')
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
        self.button_step.configure(text='Пошаговый алгоритм')
        self.button_step.pack(fill="x", pady=2, side="top")
        self.button_step.configure(command=self.build_step)
        self.button_dda = ttk.Button(frame3)
        self.button_dda.configure(text='Алгоритм DDA')
        self.button_dda.pack(fill="x", pady=2, side="top")
        self.button_dda.configure(command=self.build_dda)
        self.button_bres = ttk.Button(frame3)
        self.button_bres.configure(text='Алгоритм Брезенхема')
        self.button_bres.pack(fill="x", pady=2, side="top")
        self.button_bres.configure(command=self.build_bres)
        self.button_bres_circle = ttk.Button(frame3)
        self.button_bres_circle.configure(
            text='Алгоритм Брезенхема(окружность)')
        self.button_bres_circle.pack(fill="x", pady=2, side="top")
        self.button_bres_circle.configure(command=self.build_circle)
        separator1 = ttk.Separator(frame3)
        separator1.configure(orient="horizontal")
        separator1.pack(pady=5, side="top")
        label5 = ttk.Label(frame3)
        label5.configure(text='Scale')
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
        self.coord_x1.insert(0, '9')
        self.coord_y1.insert(0, '-5')
        self.coord_x2.insert(0, '-5')
        self.coord_y2.insert(0, '2')
        self.dots = []
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

    def draw_dot(self, x, y, color="red"):
        # fill one square of the grid with color
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        x_spacing = width / (2 * self.scale)
        y_spacing = x_spacing

        x = width / 2 + x * x_spacing
        y = height / 2 - y * y_spacing

        self.canvas.create_rectangle(x, y, x + x_spacing, y - y_spacing, fill=color)

    def update_dots(self):
        for dot in self.dots:
            self.draw_dot(dot[0], dot[1])

    def update_all(self, event=None):
        self.canvas.delete("all")
        self.update_scale(event)
        self.draw_grid()
        self.draw_axes()
        self.update_dots()
    # endregion

    def get_dots(self, circle=False):
        try:
            arr = []
            for input_el in (self.coord_x1, self.coord_y1, self.coord_x2, self.coord_y2):
                arr.append(float(input_el.get().replace(',', '.')))
            if arr[0] == arr[2] and arr[1] == arr[3] and not circle:
                self.show_alert()
                return None
            return tuple(arr)
        except:
            self.show_alert()
            return None

    def build_step(self):
        # пошаговый алгортим: двигаем с заданным шагом из точки 1 в точку 2
        # постепенно увеличиваем x и y на шаг и округляем
        self.dots = []
        start_dots = self.get_dots()
        if start_dots is None:
            return
        x1, y1, x2, y2 = start_dots
        dx = x2 - x1
        dy = y2 - y1
        parts = max(abs(dx), abs(dy)) * 10
        x_inc = dx / parts
        y_inc = dy / parts
        x = x1
        y = y1
        for i in range(int(parts+1)):
            self.dots.append((round(x), round(y)))
            x += x_inc
            y += y_inc
        # normalize dots
        self.dots = list(set(self.dots))
        self.update_all()


    def build_dda(self):
        # алгоритм DDA
        self.dots = []
        start_dots = self.get_dots()
        if start_dots is None:
            return
        x1, y1, x2, y2 = start_dots
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_inc = dx / steps
        y_inc = dy / steps
        x = x1
        y = y1
        for i in range(int(steps+1)):
            self.dots.append((round(x), round(y)))
            x += x_inc
            y += y_inc
        self.update_all()

    def build_bres(self):
        # алгоритм Брезенхема
        self.dots = []
        start_dots = self.get_dots()
        if start_dots is None:
            return
        x1, y1, x2, y2 = start_dots
        dx = x2 - x1
        dy = y2 - y1
        x_inc = 1 if dx > 0 else -1
        y_inc = 1 if dy > 0 else -1
        dx = abs(dx)
        dy = abs(dy)
        if dx > dy:
            # x - основная ось
            d = 2 * dy - dx
            d1 = 2 * dy
            d2 = 2 * (dy - dx)
            x = x1
            y = y1
            self.dots.append((x, y))
            for i in range(round(dx)):
                if d < 0:
                    d += d1
                else:
                    d += d2
                    y += y_inc
                x += x_inc
                self.dots.append((x, y))
        else:
            # y - основная ось
            d = 2 * dx - dy
            d1 = 2 * dx
            d2 = 2 * (dx - dy)
            x = x1
            y = y1
            self.dots.append((x, y))
            for i in range(round(dy)):
                if d < 0:
                    d += d1
                else:
                    d += d2
                    x += x_inc
                y += y_inc
                self.dots.append((x, y))
        self.update_all()

    # алгоритм Брезенхема (окружность радиуса x2 со смещением центра в точку (x1, y1))
    def build_circle(self):
        self.dots = []
        start_dots = self.get_dots(circle=True)
        if start_dots is None:
            return
        x1, y1, x2, y2 = start_dots
        if x2 <= 0:
            self.show_alert()
            return
        x = 0
        y = x2
        d = 3 - 2 * x2
        self.dots.append((x, y))
        while x <= y:
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1
            self.dots.append((x, y))
        self.dots += [(y, x) for x, y in self.dots]
        self.dots += [(-x, y) for x, y in self.dots]
        self.dots += [(x, -y) for x, y in self.dots]
        self.dots += [(-x, -y) for x, y in self.dots]
        self.dots = [(x1 + x, y1 + y) for x, y in self.dots]
        self.update_all()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1000x600')
    root.title('Растеризация')
    root.minsize(600, 500)
    app = UiApp(root)
    app.run()
