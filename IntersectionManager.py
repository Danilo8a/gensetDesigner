from FunctionPoints import FunctionPoints
from Function import Function
from sympy import solve, Symbol, nsolve


def num_intersect(f_1, f_2, solve_range: tuple):
    # Comprueba que las dos funciones sean instancias de Function.
    if not (isinstance(f_1, Function) and isinstance(f_2, Function)):
        raise AttributeError('The function "fun_intersect", solves the intersection between two instances of Function.')
    if f_1.is_constant() and f_2.is_constant():
        return None
    else:
        if not f_2.is_constant() and not f_1.is_constant():
            # Comprueba que tengan la misma variable independiente
            if not list(f_1.get_fun().free_symbols)[0] == list(f_2.get_fun().free_symbols)[0]:
                raise AttributeError('Only functions with the same independent variable can be intercepted. ')
        return float(nsolve(f_1.get_fun() - f_2.get_fun(), solve_range, solver='bisect', verify=False))


def num_fun_points(f_1: Function, f_2: FunctionPoints):
    if not (isinstance(f_1, Function) and isinstance(f_2, FunctionPoints)):
        raise AttributeError('The function "fun_and_point", solves '
                             'the intersection between Function and FunctionPoints instances.')
    out_array = []
    for i in range(len(f_2.get_x()) - 1):
        x_1 = f_2.get_x()[i]
        x_2 = f_2.get_x()[i + 1]
        y_1 = f_2.get_y()[i]
        y_2 = f_2.get_y()[i + 1]
        if f_1.eval(x_1) is None or f_1.eval(x_2) is None:
            continue
        elif (y_1 < f_1.eval(x_1) and y_2 < f_1.eval(x_2)) or (y_1 > f_1.eval(x_1) and y_2 > f_1.eval(x_2)):
            continue
        else:
            if x_1 == x_2 and min(y_1, y_2) <= f_1.eval(x_1) <= max(y_1, y_2):
                out_array.append(f_1.eval(x_1))
            else:
                m = (y_2 - y_1) / (x_2 - x_1)
                rect = m * Symbol('x') + m * x_1 - y_1
                out = float(nsolve(f_1.get_fun() - rect, (min(x_1, x_2), max(x_1, x_2)), solver='bisect', verify=False))
                out_array.append(out)
                out_array.sort()
    return out_array


def fun_intersect(f_1, f_2, tell_me_domain=False, solution_domain=1000):
    # Comprueba que las dos funciones sean instancias de Function.
    if not (isinstance(f_1, Function) and isinstance(f_2, Function)):
        raise AttributeError('The function "fun_intersect", solves the intersection between two instances of Function.')
    aux_out = []
    # Para dos funciones constantes, devuelve una lista vacía
    if f_1.is_constant() and f_2.is_constant():
        return aux_out
    else:
        if not f_2.is_constant() and not f_1.is_constant():
            # Comprueba que tengan la misma variable independiente
            if not list(f_1.get_fun().free_symbols)[0] == list(f_2.get_fun().free_symbols)[0]:
                raise AttributeError('Only functions with the same independent variable can be intercepted. ')
        out = solve(f_2.get_fun() - f_1.get_fun())
        for x_i in out:
            try:
                if -solution_domain <= x_i <= solution_domain:
                    aux_out.append(float(x_i))
            except TypeError:
                if tell_me_domain:
                    aux_out.append('ComplexRoot')
        return aux_out


def fun_and_point(f_1: Function, f_2: FunctionPoints, operation='speed'):
    if operation != 'speed' and operation != 'heavy':
        operation = 'speed'
    if not (isinstance(f_1, Function) and isinstance(f_2, FunctionPoints)):
        raise AttributeError('The function "fun_and_point", solves '
                             'the intersection between Function and FunctionPoints instances.')
    out_array = []
    if operation == 'speed':
        for i in range(len(f_2.get_x()) - 1):
            x_1 = f_2.get_x()[i]
            x_2 = f_2.get_x()[i + 1]
            y_1 = f_2.get_y()[i]
            y_2 = f_2.get_y()[i + 1]
            if f_1.eval(x_1) is None or f_1.eval(x_2) is None:
                continue
            elif (y_1 < f_1.eval(x_1) and y_2 < f_1.eval(x_2)) or (y_1 > f_1.eval(x_1) and y_2 > f_1.eval(x_2)):
                continue
            else:
                if x_1 == x_2 and min(y_1, y_2) <= f_1.eval(x_1) <= max(y_1, y_2):
                    out_array.append(f_1.eval(x_1))
                else:
                    m = (y_2 - y_1) / (x_2 - x_1)
                    out = solve(f_1.get_fun() - m * Symbol('x') + m * x_1 - y_1)
                    for x_i in out:
                        try:
                            aux = float(x_i)
                            if min(x_1, x_2) <= aux <= max(x_1, x_2):
                                out_array.append(float(aux))
                        except TypeError:
                            pass

    elif operation == 'heavy':
        for i in range(len(f_2.get_x()) - 1):
            x_1 = f_2.get_x()[i]
            x_2 = f_2.get_x()[i + 1]
            y_1 = f_2.get_y()[i]
            y_2 = f_2.get_y()[i + 1]
            m = (y_2 - y_1) / (x_2 - x_1)
            out = solve(f_1.get_fun() - m * Symbol('x') + m * x_1 - y_1)
            for x_i in out:
                try:
                    aux = float(x_i)
                    if min(x_1, x_2) <= aux <= max(x_1, x_2):
                        out_array.append(aux)
                except TypeError:
                    pass
    return out_array
