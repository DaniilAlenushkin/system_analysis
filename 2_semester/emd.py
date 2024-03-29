from itertools import combinations

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

    x_for_spline = np.linspace(0, max(x)+1, len(x)+1)
    y_peak = splev(x_for_spline, spl_peak)
    y_trough = splev(x_for_spline, spl_trough)
    m = list(map(lambda coordinate_peak, coordinate_trough: (coordinate_peak+coordinate_trough)/2, y_peak, y_trough))
    last_point_c = m[-1]
    m, x_for_spline, y_peak, y_trough = m[:-1], x_for_spline[:-1], y_peak[:-1], y_trough[:-1]
    if plotting:
        plt.plot(x_for_spline, y_peak)
        plt.plot(x_for_spline, y_trough)
        plt.plot(x_for_spline, m, c='k')
        plt.show()
    return last_point_c, list(map(lambda previous, current: (previous-current), y, m))


def get_c_and_r(x, previous_r, counter_c_and_r):
    lp, c = get_ts('', '', x, previous_r, False)
    r = list(map(lambda value_previous_r, value_c: value_previous_r-value_c, previous_r, c))
    plotting_2_graphs(x, c, r, f'c{counter_c_and_r}(t)', f'r{counter_c_and_r}(t)')
    return lp, c, r


def plotting_2_graphs(x, y1, y2, title_1, title_2):
    fig, ax = plt.subplots(2, 1)
    ax[0].set_title(title_1)
    ax[0].grid()
    ax[0].plot(x, y1)
    ax[1].set_title(title_2)
    ax[1].grid()
    ax[1].plot(x, y2)
    plt.show()


def get_delta(previous_value, current_value, outer_loop=False, history=[]):
    counter_delta_numerator = 0
    counter_delta_denominator = 0
    if outer_loop:
        for i in previous_value:
            counter_delta_denominator += i ** 2
        for i in history:
            for j in range(len(i)):
                counter_delta_numerator += (i[j] - previous_value[j]) ** 2
    else:
        for value in zip(previous_value, current_value):
            counter_delta_numerator += abs(value[1] - value[0])**2
            counter_delta_denominator += value[0]**2
    return counter_delta_numerator / counter_delta_denominator


def prediction(last_points_c, y_point_for_prediction):
    dict_results = {}
    for elements in [list(combinations(range(len(last_points_c)), i)) for i in range(1, len(last_points_c)+1)]:
        for element in elements:
            sum_element = 0
            for index in element:
                sum_element += last_points_c[index]
            dict_results[element] = abs(sum_element - y_point_for_prediction[1])
    minimal_k = min(dict_results.values())
    print(f'Minimal comparison factor {minimal_k}')
    print('The best prediction is:')
    for i in [i for i in dict_results.keys() if dict_results.get(i) == minimal_k]:
        for value in i:
            print(f'C{value}', end='') if value == i[0] else print(f'+C{value}', end='')
        print()


if __name__ == '__main__':
    wb = openpyxl.load_workbook('platinum_3_years.xlsx')
    current_sheet = wb.sheetnames[0]
    rows_numbers = int(wb.worksheets[0].dimensions[4:]) + 1
    x_data = [wb[current_sheet][f'A{i}'].value for i in range(2, rows_numbers)][::-1]
    y_data = [wb[current_sheet][f'B{i}'].value for i in range(2, rows_numbers)][::-1]
    x_form = [0, ]
    epsilon_internal = 0.1
    epsilon_external = 0.13
    for i in range(1, len(x_data)):
        x_form.append(x_form[-1] + abs((x_data[i] - x_data[i-1]).days))
    prediction_point = [x_form[-1], y_data[-1]]
    y_data, x_form = y_data[:-1], x_form[:-1]
    last_point, imf_1 = get_ts('Platinum (Bank of Russia)', 'y(t)', x_form, y_data)
    current_imf = imf_1
    counter = 2
    while True:
        previous_imf = current_imf
        last_point, current_imf = get_ts(f'TS {counter}', f'TS {counter}', x_form, current_imf)
        if get_delta(previous_imf, current_imf) < epsilon_internal:
            current_n = counter
            break
        counter += 1
    c_arr = [current_imf, ]
    current_c = current_imf
    current_r = list(map(lambda x, y: x-y, y_data, current_c))
    plotting_2_graphs(x_form, current_c, current_r, 'c1(t)', 'r1(t)')
    r_arr = [current_r, ]
    last_points = [last_point, ]
    counter = 2
    while True:
        previous_r = current_r[:]
        last_point, current_c, current_r = get_c_and_r(x_form, current_r, counter)
        c_arr.append(current_c)
        r_arr.append(current_r)
        last_points.append(last_point)
        if get_delta(previous_r, current_r) < epsilon_internal and \
                get_delta(previous_r, current_r, outer_loop=True, history=r_arr) > epsilon_external:
            break
        counter += 1
    check_result = current_r[:]
    for i in c_arr:
        check_result = list(map(lambda first_list_value, second_list_value:
                                first_list_value + second_list_value, i, check_result))
    plotting_2_graphs(x_form, y_data, check_result, 'Исходный график', 'Восстановленный график')
    prediction(last_points, prediction_point)
