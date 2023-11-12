from sympy import Float, Expr


class Function:

    def __init__(self, my_sym_function):
        if isinstance(my_sym_function, int) or isinstance(my_sym_function, float):
            self.__function = Float(my_sym_function)
        elif isinstance(my_sym_function, Expr):
            if len(my_sym_function.free_symbols) == 1:
                self.__function = my_sym_function
            else:
                raise AttributeError('This data structure only handles functions '
                                     'of one variable y = f(x) or constant functions y = k.')
        else:
            raise AttributeError('The function must be an integer, a float or a Sympy expression.')

    def __str__(self):
        return self.__function.__str__()

    def eval(self, x: float, domain='real', tell_me_domain=False):
        if self.is_constant():
            return float(self.__function)
        if domain == 'real':
            try:
                return float(self.__function.evalf(subs={list(self.__function.free_symbols)[0]: x}))
            except TypeError as te:
                if tell_me_domain:
                    return 'ComplexResult'
        elif domain == 'complex':
            return self.__function.evalf(subs={list(self.__function.free_symbols)[0]: x})
        else:
            raise AttributeError('The "domain" attribute must be specified as "real" or "complex".')

    def is_constant(self):
        return True if isinstance(self.__function, Float) else False

    def eval_an_array(self, x_in, domain='real', tell_me_domain=False):

        if isinstance(x_in, list):
            aux_list_returned = []
            for val in x_in:
                res_aux = self.eval(val, domain=domain, tell_me_domain=tell_me_domain)
                if res_aux is not None:
                    aux_list_returned.append(res_aux)
            return aux_list_returned
        else:
            raise AttributeError('The "x_in" attribute must be a list of numbers.')

    def get_fun(self):
        return self.__function




