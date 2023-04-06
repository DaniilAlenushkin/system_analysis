import warnings

import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings('ignore')


def plotting(predict_value, legend_predict, method_name, mse, parameters = ''):
    predict_x = [x_data[-1], x_data[-1]+1]
    predict_y = [y_data[-1], predict_value]
    fig, ax = plt.subplots()
    ax.set_title('Inflation in Russia for 15 years')
    ax.set_xlabel('Months')
    ax.set_ylabel('%')
    ax.grid()
    ax.plot(x_data, y_data)
    ax.plot(predict_x, predict_y, c='r')
    ax.legend(('Inflation in Russia for 15 years',
               legend_predict))
    plt.show()
    print(f'The inflation forecast in Russia using the {method_name} {parameters} '
          f'for February 2023 is {predict_y[-1]}% with MSE = {mse}')


def plotting_smoothing_and_prediction(smoothing_x, smoothing_y,
                                      predict_x, predict_y,
                                      legend_smoothing, legend_predict):
    fig, ax = plt.subplots()
    ax.set_title('Inflation in Russia for 15 years')
    ax.set_xlabel('Months')
    ax.set_ylabel('%')
    ax.grid()
    ax.plot(x_data, y_data)
    ax.plot(predict_x, predict_y, c='r')
    ax.plot(smoothing_x, smoothing_y)
    ax.legend(('Inflation in Russia for 15 years',
               legend_predict,
               legend_smoothing))
    plt.show()


def print_information(predict_y, method_name, parameters, mse):
    print(f'The inflation forecast in Russia using the {method_name} {parameters} '
          f'for February 2023 is {predict_y[-1]}% with MSE = {mse}')


def moving_average_method(time_series_y):
    predicts = [sum(time_series_y[-window_size:])/window_size for window_size in range(1, len(time_series_y)+1)]
    mse_values = [abs(target_value - i) for i in predicts]
    best_windows_size = mse_values.index(min(mse_values)) + 1

    def get_moving_average(win_size):
        return [sum(time_series_y[i-win_size:i])/win_size
                   for i in range(win_size, len(time_series_y))]

    prediction_y = get_moving_average(best_windows_size)
    prediction_x = x_data[best_windows_size + 1:] + [x_data[-1] + 1]

    smoothing_windows_size = 7
    smoothing_y = get_moving_average(smoothing_windows_size)
    smoothing_x = x_data[smoothing_windows_size:]

    plotting_smoothing_and_prediction(smoothing_x,
                                      smoothing_y,
                                      prediction_x,
                                      prediction_y,
                                      f'Smoothing using Moving average with a window size of {smoothing_windows_size}',
                                      f'BEST prediction using Moving average (window size = {best_windows_size})')

    print_information(prediction_y,
                      'moving average method', f'with a window size of {best_windows_size}',
                      min(mse_values))


def exponential_smoothing(time_series_y):
    alpha = np.linspace(0.1, 0.9, 9)
    predicts = []
    for a in alpha:
        predict_y = [time_series_y[0]]
        for n in range(len(time_series_y)):
            predict_y.append(a * time_series_y[n] + (1 - a) * predict_y[n])
        predicts.append(predict_y[-1])
    mse_values = [abs(target_value - i) for i in predicts]
    best_alpha = alpha[mse_values.index(min(mse_values))]

    predict_y = [time_series_y[0]]
    for i in range(len(time_series_y)):
        predict_y.append(best_alpha*time_series_y[i] + (1-best_alpha)*predict_y[i])
    predict_x = x_data + [x_data[-1]+1]

    smoothing_alpha = 0.3
    smoothing_y = [time_series_y[0]]
    for i in range(1, len(time_series_y)):
        smoothing_y.append(smoothing_alpha*time_series_y[i] + (1-smoothing_alpha)*smoothing_y[i-1])
    smoothing_x = x_data

    plotting_smoothing_and_prediction(smoothing_x,
                                      smoothing_y,
                                      predict_x,
                                      predict_y,
                                      f'Exponential smoothing with alpha equal to {smoothing_alpha}',
                                      f'BEST prediction using Exponential smoothing (alpha = {best_alpha})')

    print_information(predict_y,
                      'exponential smoothing method', f'with alpha equal to {best_alpha}',
                      min(mse_values))


def trend_method(time_series_y):
    approximations = []
    predicts = []
    for degree in range(1, 123):
        if degree == 1:
            X = sm.add_constant(np.arange(len(time_series_y)))
        else:
            X = np.column_stack([np.power(np.arange(len(time_series_y)), i) for i in range(degree + 1)])
        model = sm.OLS(time_series_y, X).fit()
        next_x = len(X)
        if degree == 1:
            next_y = model.predict([1, next_x])
        else:
            next_y = model.predict(np.power(next_x, range(degree + 1)))
        approximations.append(model.rsquared)
        predicts.append(next_y[0])

    mse = [abs(target_value - i) for i in predicts]
    best_approximation = approximations.index(max(approximations)) + 1
    best_predict = mse.index(min(mse)) + 1

    X_predict = np.column_stack([np.power(np.arange(len(time_series_y)), i) for i in range(best_predict+1)])
    predict_model = sm.OLS(time_series_y, X_predict).fit()
    predictions_y = list(predict_model.predict(X_predict)) + [predicts[best_predict-1]]
    predictions_x = x_data + [len(x_data)]

    X_approximation = np.column_stack([np.power(np.arange(len(time_series_y)), i) for i in range(best_approximation+1)])
    approximation_model = sm.OLS(time_series_y, X_approximation).fit()
    approximation_y = list(approximation_model.predict(X_approximation))
    approximation_x = x_data

    plotting_smoothing_and_prediction(approximation_x,
                                      approximation_y ,
                                      predictions_x,
                                      predictions_y,
                                      f'Trend method that gives the best fit\n(polynomial degree = {best_approximation}),'
                                      f'R^2 = {round(max(approximations), 2)}',
                                      f'Trend method that gives the best prediction\n(polynomial degree = {best_predict})')

    print_information(predictions_y,
                      'trend method', f'with polynomial degree equal to {best_predict}',
                      min(mse))


def ar_method(time_series_y):
    ts_array = np.array(time_series_y)
    predicts = []
    for p in range(1, 60):
        model = AutoReg(ts_array, lags=p)
        ar_model = model.fit()
        predicts.append(ar_model.predict(len(ts_array), len(ts_array))[0])
    mse_values = [abs(target_value - i) for i in predicts]
    plotting(predicts[mse_values.index(min(mse_values))],
             f'AR with p = {mse_values.index(min(mse_values))+1}',
             'AR method',
             min(mse_values),
             f'with p = {mse_values.index(min(mse_values))+1}')


def ma_method(time_series_y):
    predicts = []
    for q in range(1, 20):
        model = ARIMA(time_series_y, order=(0, 0, q))
        model_fit = model.fit()
        resid = model_fit.resid
        predicts.append(time_series_y[-1] + resid[-1])
    mse_values = [abs(target_value - i) for i in predicts]
    plotting(predicts[mse_values.index(min(mse_values))],
             f'MA with q = {mse_values.index(min(mse_values))+1}',
             'MA method',
             min(mse_values),
             f'with q = {mse_values.index(min(mse_values))+1}')


def arima_method(time_series_y):
    p = 53
    q = 9
    d = 1
    predicts = []
    model = ARIMA(time_series_y, order=(p, d, q))
    model_fit = model.fit()
    next_value = model_fit.forecast()[0]
    predicts.append(next_value)

    mse_values = [abs(target_value - i) for i in predicts]

    plotting(predicts[mse_values.index(min(mse_values))],
             f'ARIMA with p={p}, d={mse_values.index(min(mse_values)) + 1}, q={q}',
             'ARIMA method',
             min(mse_values),
             f'with p={p}, d={mse_values.index(min(mse_values)) + 1}, q={q}')


if __name__ == '__main__':
    wb = openpyxl.load_workbook('inflation_15_years.xlsx')
    current_sheet = wb.sheetnames[0]
    rows_numbers = int(wb.worksheets[0].dimensions[4:])
    x_data = [wb[current_sheet][f'B{i}'].value for i in range(1, rows_numbers)]
    y_data = [wb[current_sheet][f'C{i}'].value for i in range(1, rows_numbers)]
    target_value = wb[current_sheet][f'C{rows_numbers}'].value
    moving_average_method(y_data)
    exponential_smoothing(y_data)
    trend_method(y_data)
    ar_method(y_data)
    ma_method(y_data)
    arima_method(y_data)
