from scipy.interpolate import make_interp_spline, interp1d
import numpy as np


class FunctionPoints:

    def __init__(self, x_array, y_array, grid=500):
        if not (isinstance(x_array, list) and isinstance(y_array, list)):
            raise AttributeError('This function must be defined by means of two arrays of points.')
        elif len(x_array) != len(y_array):
            raise AttributeError('Dot arrays must have the same number of elements.')
        else:
            arr = np.array([x_array, y_array])
            arr = arr[:, arr[0].argsort()]
            x_array = list(arr[0, :])
            y_array = list(arr[1, :])
            x_y_spline = make_interp_spline(x_array, y_array)
            x_ = np.linspace(min(x_array), max(x_array), grid)
            y_ = x_y_spline(x_)
            self.__x = list(map(float, x_))
            self.__y = list(map(float, y_))
            self.__function = interp1d(x_, y_)

    def __str__(self):
        return f'x coordinates: {self.__x} \n y coordinates: {self.__y}'

    def eval(self, value: float, no_out_range=True):
        if min(self.__x) <= value <= max(self.__x):
            return self.__function(value)
        else:
            if not no_out_range:
                raise AttributeError(f'The parameter "x" must be bounded between the extremes {self.__x[0]} y {self.__x[-1]}')

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def eval_an_array(self, x_input, tell_me_out_range=False):
        if min(x_input) < min(self.__x) or max(x_input) > max(self.__x):
            if tell_me_out_range:
                return 'Value out of range.'
            else:
                raise AttributeError(f'The parameter "x" must be bounded between the extremes {self.__x[0]} y {self.__x[-1]}')
        else:
            return self.__function(x_input)
