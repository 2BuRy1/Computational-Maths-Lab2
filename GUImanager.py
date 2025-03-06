import threading
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = None

def plot_function():
    global canvas

    for widget in frame_plot.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots()
    x = np.linspace(-2, 2, 400)

    if selected_type.get() == "Нелинейное уравнение":
        if selected_equation.get() == "sin(x) - x/2 = 0":
            y = np.sin(x) - x / 2
        elif selected_equation.get() == "x^3 - x - 1 = 0":
            y = x ** 3 - x - 1
        elif selected_equation.get() == "e^x - 3x = 0":
            y = np.exp(x) - 3 * x
        ax.plot(x, y, label=selected_equation.get())
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.legend()

    elif selected_type.get() == "Система нелинейных уравнений":
        x = np.linspace(-2, 2, 100)
        y = np.linspace(-2, 2, 100)
        X, Y = np.meshgrid(x, y)

        if selected_system.get() == "sin(x + y) - 1.4x = 0, x^2 + y^2 = 1":
            Z1 = np.sin(X + Y) - 1.4 * X
            Z2 = X ** 2 + Y ** 2 - 1
            ax.contour(X, Y, Z1, levels=[0], colors='r')
            ax.contour(X, Y, Z2, levels=[0], colors='b')
            ax.set_title("График системы уравнений")

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.get_tk_widget().pack()
    canvas.draw()


def solve(event=None):
    """Выводит выбранные данные в консоль и строит график."""
    print(f"Вы выбрали: {selected_type.get()}")
    if selected_type.get() == "Нелинейное уравнение":
        print(f"Уравнение: {selected_equation.get()}")
        print(f"Метод решения: {selected_method_for_unlinear.get()}")
    elif selected_type.get() == "Система нелинейных уравнений":
        print(f"Система: {selected_system.get()}")
    plot_function()


def update_options(event):
    equation_label.pack_forget()
    equation_menu.pack_forget()
    system_label.pack_forget()
    system_menu.pack_forget()
    method_label.pack_forget()
    method_menu.pack_forget()
    if selected_type.get() == "Нелинейное уравнение":
        equation_label.pack()
        equation_menu.pack()
        method_label.pack()
        method_menu.pack()
    elif selected_type.get() == "Система нелинейных уравнений":
        system_label.pack()
        system_menu.pack()
        method_label.pack_forget()
        method_menu.pack_forget()
    plot_function()


def setData():
    global data
    print("set data")
    if selected_type.get() == "Нелинейное уравнение":
        data = False, selected_equation.get(), selected_method_for_unlinear.get()
    else:
        data = True,selected_system.get()


def getData():
    return data

root = tk.Tk()
root.title("Решение нелинейных уравнений")
root.geometry("600x600")

frame_controls = tk.Frame(root)
frame_controls.pack(pady=10)

frame_plot = tk.Frame(root)
frame_plot.pack(pady=10)

selected_type = tk.StringVar()
type_label = tk.Label(frame_controls, text="Выберите тип задачи:")
type_label.pack()
type_menu = ttk.Combobox(frame_controls, textvariable=selected_type,
                             values=["Нелинейное уравнение", "Система нелинейных уравнений"])
type_menu.pack()
type_menu.bind("<<ComboboxSelected>>", update_options)

selected_equation = tk.StringVar()
equation_label = tk.Label(frame_controls, text="Выберите уравнение:")
equation_menu = ttk.Combobox(frame_controls, textvariable=selected_equation,
                                 values=["sin(x) - x/2 = 0", "x^3 - x - 1 = 0", "e^x - 3x = 0"])
equation_menu.bind("<<ComboboxSelected>>", solve)

selected_system = tk.StringVar()
system_label = tk.Label(frame_controls, text="Выберите систему уравнений:")
system_menu = ttk.Combobox(frame_controls, textvariable=selected_system,
                               values=["sin(x + y) - 1.4x = 0, x^2 + y^2 = 1"])
system_menu.bind("<<ComboboxSelected>>", solve)

selected_method_for_unlinear = tk.StringVar()
method_label = tk.Label(frame_controls, text="Выберите метод решения:")
method_label.pack()
method_menu = ttk.Combobox(frame_controls, textvariable=selected_method_for_unlinear,
                               values=["Метод простых итераций", "Метод Ньютона", "Метод половинного деления"])
method_menu.pack()
method_menu.bind("<<ComboboxSelected>>", solve)

solve_button = tk.Button(frame_controls, text="Отправить", command=setData)
solve_button.pack()



def start():
   root.mainloop()

