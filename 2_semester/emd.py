import matplotlib.pyplot as plt
import numpy as np
import openpyxl
from scipy.signal import find_peaks
from scipy.interpolate import splrep, splev


def get_ts(title, first_arg_legend,  x, y, plotting=True):
    if plotting:
        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.plot(x, y)
        ax.grid()
        if title == 'Platinum (Bank of Russia)':
            ax.set_xlabel('Days')
            ax.set_ylabel('Ruble/Gram')
        plt.tick_params(labelsize=8)
    peak_locations = find_peaks(y)
    trough_locations = find_peaks(list(map(lambda val: -val, y)))
    if plotting:
        ax.scatter([x[i] for i in peak_locations[0]], [y[i] for i in peak_locations[0]], s=10, c='r')
        ax.scatter([x[i] for i in trough_locations[0]], [y[i] for i in trough_locations[0]], s=10, c='y')
        ax.legend((first_arg_legend, 'max', 'min'))

    form_peak_locations = [[x[i] for i in peak_locations[0]], [y[i] for i in peak_locations[0]]]
    form_trough_locations = [[x[i] for i in trough_locations[0]], [y[i] for i in trough_locations[0]]]

    if y[0] < form_peak_locations[1][0] and y[0] < form_trough_locations[1][0]:
        form_trough_locations[1].insert(0, y[0])
        form_trough_locations[0].insert(0, x[0])
        form_peak_locations[1].insert(0, form_peak_locations[1][0])
        form_peak_locations[0].insert(0, x[0])

    elif y[0] > form_peak_locations[1][0] and y[0] > form_trough_locations[1][0]:
        form_trough_locations[1].insert(0, form_trough_locations[1][0])
        form_trough_locations[0].insert(0, x[0])
        form_peak_locations[1].insert(0, y[0])
        form_peak_locations[0].insert(0, x[0])

    elif form_trough_locations[1][0] < y[0] < form_peak_locations[1][0]:
        form_trough_locations[1].insert(0, form_trough_locations[1][0])
        form_trough_locations[0].insert(0, x[0])
        form_peak_locations[1].insert(0, form_peak_locations[1][0])
        form_peak_locations[0].insert(0, x[0])

    if y[-1] < form_peak_locations[1][-1] and y[-1] < form_trough_locations[1][-1]:
        form_trough_locations[1].append(y[-1])
        form_trough_locations[0].append(x[-1])
        form_peak_locations[1].append(form_peak_locations[1][-1])
        form_peak_locations[0].append(x[-1])

    elif y[-1] > form_peak_locations[1][-1] and y[-1] > form_trough_locations[1][-1]:
        form_trough_locations[1].append(form_trough_locations[1][-1])
        form_trough_locations[0].append(x[-1])
        form_peak_locations[1].append(y[-1])
        form_peak_locations[0].append(x[-1])

    elif form_trough_locations[1][-1] < y[-1] < form_peak_locations[1][-1]:
        form_trough_locations[1].append(form_trough_locations[1][-1])
        form_trough_locations[0].append(x[-1])
        form_peak_locations[1].append(form_peak_locations[1][-1])
        form_peak_locations[0].append(x[-1])

    try:
        spl_peak = splrep(np.array(form_peak_locations[0]),
                          np.array(form_peak_locations[1]))
    except TypeError:
        spl_peak = splrep(np.array(form_peak_locations[0]),
                          np.array(form_peak_locations[1]),
                          k=2)

    try:
        spl_trough = splrep(np.array(form_trough_locations[0]),
                            np.array(form_trough_locations[1]))
    except TypeError:
        spl_trough = splrep(np.array(form_trough_locations[0]),
                            np.array(form_trough_locations[1]),
                            k=2)

    x_for_spline = np.linspace(0, max(x), len(x))
    y_peak = splev(x_for_spline, spl_peak)
    y_trough = splev(x_for_spline, spl_trough)
    m = list(map(lambda coordinate_peak, coordinate_trough: (coordinate_peak+coordinate_trough)/2, y_peak, y_trough))
    if plotting:
        plt.plot(x_for_spline, y_peak)
        plt.plot(x_for_spline, y_trough)
        plt.plot(x_for_spline, m, c='k')
        plt.show()
    return list(map(lambda previous, current: (previous-current), y, m))


def get_c_and_r(x, previous_r, counter_c_and_r):
    c = get_ts('', '', x, previous_r, False)
    r = list(map(lambda value_previous_r, value_c: value_previous_r-value_c, previous_r, c))
    plotting_2_graphs(x, c, r, f'c{counter_c_and_r}(t)', f'r{counter_c_and_r}(t)')
    return c, r


def plotting_2_graphs(x, y1, y2, title_1, title_2):
    fig, ax = plt.subplots(2, 1)
    ax[0].set_title(title_1)
    ax[0].grid()
    ax[0].plot(x, y1)
    ax[1].set_title(title_2)
    ax[1].grid()
    ax[1].plot(x, y2)
    plt.show()


if __name__ == '__main__':
    wb = openpyxl.load_workbook('platinum_3_years.xlsx')
    current_sheet = wb.sheetnames[0]
    rows_numbers = int(wb.worksheets[0].dimensions[4:]) + 1
    x_data = [wb[current_sheet][f'A{i}'].value for i in range(2, rows_numbers)]
    y_data = [wb[current_sheet][f'B{i}'].value for i in range(2, rows_numbers)]
    x_form = [0, ]
    for i in range(1, len(x_data)):
        x_form.append(x_form[-1] + abs((x_data[::-1][i] - x_data[::-1][i-1]).days))
    imf_1 = get_ts('Platinum (Bank of Russia)', 'y(t)', x_form, y_data[::-1])
    current_imf = imf_1
    counter = 2
    while True:
        previous_imf = current_imf
        current_imf = get_ts(f'TS {counter}', f'TS {counter}', x_form, current_imf)
        counter_sigma_numerator = 0
        counter_sigma_denominator = 0
        for value in zip(previous_imf, current_imf):
            counter_sigma_numerator += abs(value[1] - value[0])**2
            counter_sigma_denominator += value[0]**2
        delta = counter_sigma_numerator / counter_sigma_denominator
        if delta < 0.1:
            current_n = counter
            break
        counter += 1
    c_arr = [current_imf, ]
    current_c = current_imf
    current_r = list(map(lambda x, y: x-y, y_data[::-1], current_c))
    plotting_2_graphs(x_form, current_c, current_r, 'c1(t)', 'r1(t)')
    for i in range(2, 8):
        current_c, current_r = get_c_and_r(x_form, current_r, i)
        c_arr.append(current_c)
    check_result = current_r[:]
    for i in c_arr:
        check_result = list(map(lambda first_list_value, second_list_value:
                                first_list_value + second_list_value, i, check_result))
    plotting_2_graphs(x_form, y_data[::-1], check_result, 'Исходный график', 'Восстановленный график')
