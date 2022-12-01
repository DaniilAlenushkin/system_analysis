#  Laboratory work №4
import matplotlib.pyplot as plt
from numpy import arange
import threading
from tkinter import *
import warnings

warnings.filterwarnings('ignore')


class App(Tk):
    def __init__(self):
        # Rendering the application window
        super().__init__()
        self.bg = '#afeeee'
        self.title("Laboratory work №4")
        self.configure(background=self.bg)
        self.number_of_values = 1100  # Number of values by x
        self.row = (i for i in range(13))
        self.cm = 1 / 2.54

        self.lbl_empty = Label(self, text='  ', background=self.bg)
        self.lbl_empty.grid(column=0, row=0, rowspan=10)

        self.lbl_empty = Label(self, text='  ', background=self.bg)
        self.lbl_empty.grid(column=2, row=0, rowspan=10)

        self.lbl_greeting = Label(self, text='Laboratory work №4', background=self.bg)
        self.lbl_greeting.grid(column=1, row=next(self.row))

        self.lbl_greeting = Label(self, text='Variant №1', background=self.bg)
        self.lbl_greeting.grid(column=1, row=next(self.row))

        self.delay_state = BooleanVar()
        self.delay_state.set(False)
        self.delay = Checkbutton(self, text='Build graphs with a delay?', variable=self.delay_state, bg=self.bg)
        self.delay.grid(column=1, row=next(self.row))

        self.lbl_empty = Label(self, text='         ', background=self.bg)
        self.lbl_empty.grid(column=1, row=next(self.row))

        self.btn_first_point = Button(self, text="Execute the first point", width=20,
                                      command=lambda: self.clicked_some_point(self.btn_first_point,
                                                                              self.first_point))
        self.btn_first_point.grid(column=1, row=next(self.row))

        self.lbl_empty = Label(self, text='         ', background=self.bg)
        self.lbl_empty.grid(column=1, row=next(self.row))

        self.btn_second_point = Button(self, text="Execute the second point", width=20,
                                       command=lambda: self.clicked_some_point(self.btn_second_point,
                                                                               self.second_point))
        self.btn_second_point.grid(column=1, row=next(self.row))

        self.lbl_empty = Label(self, text='         ', background=self.bg)
        self.lbl_empty.grid(column=1, row=next(self.row))

        self.btn_third_point = Button(self, text="Execute the third point", width=20,
                                      command=lambda: self.clicked_some_point(self.btn_third_point,
                                                                              self.third_point))
        self.btn_third_point.grid(column=1, row=next(self.row))

        self.lbl_empty = Label(self, text='         ', background=self.bg)
        self.lbl_empty.grid(column=1, row=next(self.row))

        self.btn_bifurcation_diagram = Button(self, text="Build a bifurcation diagram", width=20,
                                              command=lambda: self.clicked_some_point(self.btn_bifurcation_diagram,
                                                                                      self.bifurcation_diagram))
        self.btn_bifurcation_diagram.grid(column=1, row=next(self.row))

        self.lbl_empty = Label(self, text='         ', background=self.bg)
        self.lbl_empty.grid(column=1, row=next(self.row))

        self.lbl_author = Label(self, text='Author: Alenushkin Daniil, group 4232m', background=self.bg)
        self.lbl_author.grid(column=1, row=next(self.row))

    def clicked_some_point(self, button, some_point):
        thread_some_point = threading.Thread(target=some_point, daemon=True)
        button['state'] = 'disable'
        thread_some_point.start()
        self.after(ms=1000, func=lambda: self.button_unlock(thread_some_point, button))

    def bifurcation_diagram(self):
        fig, ax = plt.subplots()
        ax.set_title('Bifurcation diagram "Feigenbaum constants"')
        ax.set_xlabel('r', loc='right')
        ax.set_ylabel('x', loc='top')
        ax.grid()
        x_arr = []
        y_arr = []
        for r in arange(3, 4.001, 0.001):
            x = [0.4, ]  # Start point
            t = [r, ]
            for c in range(1, self.number_of_values):
                x.append(r*x[c-1]*(1-x[c-1]))  # Model
                t.append(r)
            x_arr.append(t[self.number_of_values - 200:])
            y_arr.append(x[self.number_of_values - 200:])
        ax.scatter(x_arr, y_arr, s=1, c='b')  # Dot plot output
        plt.show()

    def first_point(self):
        mat = [[], [], [], []]
        for r in range(3, 5):
            x = [0.4, ]  # Start point
            for i in range(self.number_of_values):
                x.append(r * x[i] * (1 - x[i]))  # Model
                for pos in range(2):
                    # writing values into the matrix x(n) and into the matrix x(n+1)
                    mat[r + 2 * pos - 3].append(x[i + pos])
        # Plotting
        title_list = ['Graphic dependency f(x,n) for r=',
                      'Phase portrait at r=']
        axis_names = [['n', 'x'],
                      ['x(n)', 'x(n+1)']]
        chart_data = [[range(1, self.number_of_values + 1), mat[0]],
                      [range(1, self.number_of_values + 1), mat[1]],
                      [mat[0], mat[2]],
                      [mat[1], mat[3]]]
        fig, ax = plt.subplots(2, 2, figsize=(25 * self.cm, 20 * self.cm))
        if self.delay_state.get():
            fig.canvas.draw()
            plt.show(block=False)
        for graph in range(4):
            current_ax = ax[graph % 2, graph // 2]
            current_ax.set_title(f'{title_list[graph // 2]}{graph + 3 if graph < 2 else graph + 1}')
            current_ax.set_xlabel(axis_names[graph // 2][0], loc='right')
            current_ax.set_ylabel(axis_names[graph // 2][1], loc='top')
            current_ax.grid()
            if self.delay_state.get():
                current_ax.set_xlim([min(chart_data[graph][0]), max(chart_data[graph][0])])
                current_ax.set_ylim([min(chart_data[graph][1]), max(chart_data[graph][1])])
            if graph > 1:
                current_ax.scatter(chart_data[graph][0][0], chart_data[graph][1][0], s=30, c='b', alpha=1)
                current_ax.scatter(chart_data[graph][0][self.number_of_values - 1],
                                   chart_data[graph][1][self.number_of_values - 1], s=30, c='r', alpha=1)
                current_ax.legend(['Start point', 'End point'])
            if self.delay_state.get():
                line, = current_ax.plot([], alpha=0.85)
                for i in range(len(chart_data[graph][0])):
                    line.set_data(chart_data[graph][0][:i+2], chart_data[graph][1][:i+2])
                    fig.canvas.draw()
                    fig.canvas.flush_events()
                current_ax.text(min(chart_data[graph][0]), max(chart_data[graph][1]), "\n Plotting finished",
                                verticalalignment='top')
            else:
                current_ax.plot(chart_data[graph][0], chart_data[graph][1], alpha=0.85)
        plt.show()

    def second_point(self):
        mat = [[], []]
        x = [0.4, ]  # Start point
        r = 4
        for i in range(self.number_of_values):
            x.append(r * x[i] * (1 - x[i]))  # Model
            for number in range(2):
                # Writing values to a matrix with an accuracy of 15 and 2 decimal places
                mat[number].append(round(x[i], 2 if number == 0 else 15))
        # Plotting
        fig, ax = plt.subplots(1, 2, figsize=(30 * self.cm, 15 * self.cm))
        if self.delay_state.get():
            fig.canvas.draw()
            plt.show(block=False)
        for graph in range(2):
            current_ax = ax[graph % 2]
            current_ax.set_title('Graphic dependency f(x,n) for r=4')
            current_ax.grid()
            current_ax.set_xlabel('n', loc='right')
            current_ax.set_ylabel('x', loc='top')
            if self.delay_state.get():
                if graph == 1:
                    current_ax.set_xlim([540, 560])
                else:
                    current_ax.set_xlim(
                        [min(range(1, self.number_of_values + 1)), max(range(1, self.number_of_values + 1))])
                current_ax.set_ylim([min(mat[0]) if min(mat[0]) < min(mat[1]) else min(mat[1]),
                                     max(mat[0]) if max(mat[0]) > max(mat[1]) else max(mat[1])])
                line1,  = current_ax.plot([], alpha=0.85)
                line2, = current_ax.plot([], alpha=0.85)
                for i in range(len(mat[0]) if graph == 0 else len(list(range(540, 561)))):
                    if graph == 0:
                        line1.set_data(range(1, self.number_of_values + 1)[:i+2], mat[0][:i+2])
                        line2.set_data(range(1, self.number_of_values + 1)[:i + 2], mat[1][:i+2])
                    else:
                        line1.set_data(range(540, 561)[:i+2], mat[0][540:561][:i+2])
                        line2.set_data(range(540, 561)[:i+2], mat[1][540:561][:i+2])
                    fig.canvas.draw()
                    fig.canvas.flush_events()
                current_ax.text(540 if graph == 1 else min(range(1, self.number_of_values + 1)),
                                max(mat[0]), "\n Plotting finished", verticalalignment='top')
            else:
                if graph == 1:
                    plt.xlim([540, 560])
                current_ax.plot(range(1, self.number_of_values + 1), mat[0])
                current_ax.plot(range(1, self.number_of_values + 1), mat[1])
            current_ax.legend(['Precision: 2 decimal places',
                               'Precision: 15 decimal places'])
        plt.show()

    def third_point(self):
        mat = [[], [], [], []]
        x = [0.4, ]  # Start point
        r = 4
        for i in range(self.number_of_values):
            x.append(r * x[i] * (1 - x[i]))  # Model
            for number in range(4):
                # Writing values into the matrix x(n) and into the matrix x(n+1)
                # with an accuracy of 15 and 2 decimal places
                mat[number].append(round(x[i] if number in [0, 2] else x[i + 1],
                                         2 if number in [0, 1] else 15))
        # Plotting
        fig, ax = plt.subplots(1, 2, figsize=(30 * self.cm, 15 * self.cm))
        if self.delay_state.get():
            fig.canvas.draw()
            plt.show(block=False)
        for graph in range(2):
            current_ax = ax[graph % 2]
            current_ax.set_title(f'Phase portrait at r=4, accuracy {2 if graph == 0 else 15} decimal places')
            current_ax.grid()
            current_ax.set_xlabel('x(n)', loc='right')
            current_ax.set_ylabel('x(n+1)', loc='top')
            if self.delay_state.get():
                current_ax.set_xlim([min(mat[0]) if graph == 0 else min(mat[2]),
                                     max(mat[0]) if graph == 0 else max(mat[2])])
                current_ax.set_ylim([min(mat[1]) if graph == 0 else min(mat[3]),
                                     max(mat[1]) if graph == 0 else max(mat[3])])
            current_ax.scatter(mat[0][0] if graph == 0 else mat[2][0],
                               mat[1][0] if graph == 0 else mat[3][0],
                               s=30, c='b', alpha=1)
            current_ax.scatter(mat[0][self.number_of_values - 1] if graph == 0 else mat[2][self.number_of_values - 1],
                               mat[1][self.number_of_values - 1] if graph == 0 else mat[3][self.number_of_values - 1],
                               s=30, c='r', alpha=1)
            current_ax.legend(['Start point', 'End point'])
            if self.delay_state.get():
                line, = current_ax.plot([], alpha=0.85)

                for i in range(len(mat[0]) if graph == 0 else len(mat[2])):
                    line.set_data(mat[0][:i + 2] if graph == 0 else mat[2][:i + 2],
                                  mat[1][:i + 2] if graph == 0 else mat[3][:i + 2])
                    fig.canvas.draw()
                    fig.canvas.flush_events()
                current_ax.text(min(mat[0]) if graph == 0 else min(mat[2]),
                                max(mat[1]) if graph == 0 else max(mat[3]),
                                "\n Plotting finished", verticalalignment='top')
            else:
                current_ax.plot(mat[0] if graph == 0 else mat[2],
                                mat[1] if graph == 0 else mat[3],
                                alpha=0.85)
        plt.show()

    def button_unlock(self, current_thread, current_button):
        # Function to unlock the button after closing the figure
        if not current_thread.is_alive():
            current_button['state'] = 'active'
        else:
            self.after(ms=1000, func=lambda: self.button_unlock(current_thread, current_button))


if __name__ == '__main__':
    window = App()
    window.mainloop()
