#  Laboratory work №4
import matplotlib.pyplot as plt
from numpy import arange
import threading
from tkinter import *
import warnings

warnings.filterwarnings('ignore')


class App(Tk):
    def __init__(self):
        super().__init__()
        self.bg = '#afeeee'
        self.title("Laboratory work №4")
        self.configure(background=self.bg)
        self.number_of_values = 1100
        self.row = (i for i in range(12))
        self.cm = 1 / 2.54

        self.lbl_empty = Label(self, text='  ', background=self.bg)
        self.lbl_empty.grid(column=0, row=0, rowspan=10)
        self.lbl_empty = Label(self, text='  ', background=self.bg)
        self.lbl_empty.grid(column=2, row=0, rowspan=10)

        self.lbl_greeting = Label(self, text='Laboratory work №4', background=self.bg)
        self.lbl_greeting.grid(column=1, row=next(self.row))

        self.lbl_greeting = Label(self, text='Variant №1', background=self.bg)
        self.lbl_greeting.grid(column=1, row=next(self.row))

        self.lbl_empty = Label(self, text='         ', background=self.bg)
        self.lbl_empty.grid(column=1, row=next(self.row))

        self.btn_first_point = Button(self, text="Execute the first point", width=20, command=self.clicked_first_point)
        self.btn_first_point.grid(column=1, row=next(self.row))

        self.lbl_empty = Label(self, text='         ', background=self.bg)
        self.lbl_empty.grid(column=1, row=next(self.row))

        self.btn_second_point = Button(self, text="Execute the second point", width=20,
                                       command=self.clicked_second_point)
        self.btn_second_point.grid(column=1, row=next(self.row))

        self.lbl_empty = Label(self, text='         ', background=self.bg)
        self.lbl_empty.grid(column=1, row=next(self.row))

        self.btn_third_point = Button(self, text="Execute the third point", width=20, command=self.clicked_third_point)
        self.btn_third_point.grid(column=1, row=next(self.row))

        self.lbl_empty = Label(self, text='         ', background=self.bg)
        self.lbl_empty.grid(column=1, row=next(self.row))

        self.btn_bifurcation_diagram = Button(self, text="Build a bifurcation diagram", width=20,
                                              command=self.clicked_bifurcation_diagram)
        self.btn_bifurcation_diagram.grid(column=1, row=next(self.row))

        self.lbl_empty = Label(self, text='         ', background=self.bg)
        self.lbl_empty.grid(column=1, row=next(self.row))

        self.lbl_author = Label(self, text='Author: Alenushkin Daniil, group 4232m', background=self.bg)
        self.lbl_author.grid(column=1, row=next(self.row))

    def clicked_first_point(self):
        thread_first_point = threading.Thread(target=self.first_point, daemon=True)
        self.btn_first_point['state'] = 'disabled'
        thread_first_point.start()
        self.after(ms=1000, func=lambda: self.button_unlock(thread_first_point, self.btn_first_point))

    def clicked_second_point(self):
        thread_second_point = threading.Thread(target=self.second_point, daemon=True)
        self.btn_second_point['state'] = 'disabled'
        thread_second_point.start()
        self.after(ms=1000, func=lambda: self.button_unlock(thread_second_point, self.btn_second_point))

    def clicked_third_point(self):
        thread_third_point = threading.Thread(target=self.third_point, daemon=True)
        self.btn_third_point['state'] = 'disabled'
        thread_third_point.start()
        self.after(ms=1000, func=lambda: self.button_unlock(thread_third_point, self.btn_third_point))

    def clicked_bifurcation_diagram(self):
        thread_bifurcation_diagram = threading.Thread(target=self.bifurcation_diagram, daemon=True)
        self.btn_bifurcation_diagram['state'] = 'disabled'
        thread_bifurcation_diagram.start()
        self.after(ms=1000, func=lambda: self.button_unlock(thread_bifurcation_diagram,
                                                          self.btn_bifurcation_diagram))

    def bifurcation_diagram(self):
        fig, ax = plt.subplots()
        ax.set_title('Bifurcation diagram "Feigenbaum constants"')
        ax.set_xlabel('r', loc='right')
        ax.set_ylabel('x', loc='top')
        ax.grid()
        for r in arange(3, 4.001, 0.001):
            x = [0.4, ]
            t = [r, ]
            for c in range(1, self.number_of_values):
                x.append(r * x[c - 1] * (1 - x[c - 1]))
                t.append(r)
            ax.scatter(t[self.number_of_values - 200:], x[self.number_of_values - 200:], s=1, c='b')
        plt.show()

    def first_point(self):
        mat = [[], [], [], []]
        for r in range(3, 5):
            x = [0.4, ]
            for i in range(self.number_of_values):
                x.append(r * x[i] * (1 - x[i]))
                for pos in range(2):
                    mat[r + 2 * pos - 3].append(x[i + pos])
        title_list = ['Graphic dependency f(x,r) for r=',
                      'Phase portrait at r=']
        axis_names = [['x', 'r'],
                      ['x(n)', 'x(n+1)']]
        chart_data = [[range(1, self.number_of_values + 1), mat[0]],
                      [range(1, self.number_of_values + 1), mat[1]],
                      [mat[0], mat[2]],
                      [mat[1], mat[3]]]
        fig, ax = plt.subplots(2, 2, figsize=(25 * self.cm, 20 * self.cm))
        for graph in range(4):
            current_ax = ax[graph % 2, graph // 2]
            current_ax.set_title(f'{title_list[graph // 2]}{graph + 3 if graph < 2 else graph + 1}')
            current_ax.set_xlabel(axis_names[graph // 2][0], loc='right')
            current_ax.set_ylabel(axis_names[graph // 2][1], loc='top')
            current_ax.grid()
            if graph > 1:
                current_ax.scatter(chart_data[graph][0][0], chart_data[graph][1][0], s=30, c='b', alpha=1)
                current_ax.scatter(chart_data[graph][0][self.number_of_values - 1],
                                   chart_data[graph][1][self.number_of_values - 1], s=30, c='r', alpha=1)
                current_ax.legend(['Start point', 'End point'])
            current_ax.plot(chart_data[graph][0], chart_data[graph][1], alpha=0.85)
        plt.show()

    def second_point(self):
        mat = [[], []]
        x = [0.4, ]
        r = 4
        for i in range(self.number_of_values):
            x.append(r * x[i] * (1 - x[i]))
            for number in range(2):
                mat[number].append(round(x[i], 2 if number == 0 else 15))
        fig, ax = plt.subplots(1, 2, figsize=(30 * self.cm, 15 * self.cm))
        for graph in range(2):
            current_ax = ax[graph % 2]
            current_ax.set_title('Graphic dependency f(x,r) for r=4')
            current_ax.grid()
            current_ax.set_xlabel('x', loc='right')
            current_ax.set_ylabel('r', loc='top')
            if graph == 1:
                plt.xlim(0, 150)
                plt.ylim(0, 0.05)
            current_ax.plot(range(1, self.number_of_values + 1), mat[0])
            current_ax.plot(range(1, self.number_of_values + 1), mat[1])
            current_ax.legend(['Precision: 2 decimal places',
                               'Precision: 15 decimal places'])
        plt.show()

    def third_point(self):
        mat = [[], [], [], []]
        x = [0.4, ]
        r = 4
        for i in range(self.number_of_values):
            x.append(r * x[i] * (1 - x[i]))
            for number in range(4):
                mat[number].append(round(x[i] if number in [0, 2] else x[i + 1],
                                         2 if number in [0, 1] else 15))
        fig, ax = plt.subplots(1, 2, figsize=(30 * self.cm, 15 * self.cm))
        for graph in range(2):
            current_ax = ax[graph % 2]
            current_ax.set_title(f'Phase portrait at r=4, accuracy {2 if graph == 0 else 15} decimal places')
            current_ax.grid()
            current_ax.set_xlabel('x(n)', loc='right')
            current_ax.set_ylabel('x(n+1)', loc='top')
            current_ax.scatter(mat[0][0] if graph == 0 else mat[2][0],
                               mat[1][0] if graph == 0 else mat[3][0],
                               s=30, c='b', alpha=1)
            current_ax.scatter(mat[0][self.number_of_values - 1] if graph == 0 else mat[2][self.number_of_values - 1],
                               mat[1][self.number_of_values - 1] if graph == 0 else mat[3][self.number_of_values - 1],
                               s=30, c='r', alpha=1)
            current_ax.legend(['Start point', 'End point'])
            current_ax.plot(mat[0] if graph == 0 else mat[2],
                            mat[1] if graph == 0 else mat[3],
                            alpha=0.85)
        plt.show()

    def button_unlock(self, current_thread, current_button):
        if not current_thread.is_alive():
            current_button['state'] = 'active'
        else:
            self.after(ms=1000, func=lambda: self.button_unlock(current_thread, current_button))


if __name__ == '__main__':
    window = App()
    window.mainloop()
