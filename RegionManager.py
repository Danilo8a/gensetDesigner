import gui_utils
from IPoint import IPoint
from IntersectionManager import *
from sympy import Symbol
import numpy as np


def clean_by_x(points: list[IPoint]):
    excluir = set()
    for p_i in points:
        for p_j in points:
            if p_i is p_j or p_j in excluir:
                continue
            elif min(p_i.get_x(), 0) <= p_j.get_x() <= max(p_i.get_x(), 0):
                if p_i.get_y() >= p_j.get_y():
                    excluir.add(p_i)
                    break
    return set(points) - excluir


def clean_by_y(points: list[IPoint], functions):
    excluir = set()
    for p_i in points:
        for f_i in functions:
            if f_i.eval(p_i.get_x()) is None:
                continue
            elif f_i.eval(p_i.get_x()) < p_i.get_y():
                excluir.add(p_i)
    return set(points) - excluir


def get_minor_contour(points: list[IPoint], functions: list, gas=0.0001):
    intersect = []
    exclude = []
    min_sc = None
    min_fc = None
    for p_i in points:
        if p_i.get_x() == 0:
            exclude.append(p_i)
        elif p_i.get_y() == 0:
            if p_i.get_x() < 0:

                if min_sc is None:
                    min_sc = p_i
                elif p_i.get_x() > min_sc.get_x():
                    exclude.append(min_sc)
                    min_sc = p_i
                elif p_i.get_x() == min_sc.get_x():
                    x = p_i.get_x()
                    fun_p_i = p_i.major_after()
                    fun_sc = min_sc.major_after()
                    if fun_p_i.eval(x + 0.1) > fun_sc.eval(x + 0.1):
                        exclude.append(p_i)
                    else:
                        exclude.append(min_sc)
                        min_sc = p_i
                else:
                    exclude.append(p_i)
            else:

                if min_fc is None:
                    min_fc = p_i
                elif p_i.get_x() < min_fc.get_x():
                    exclude.append(min_fc)
                    min_fc = p_i
                else:
                    exclude.append(p_i)
        else:
            for fun in functions:
                m = float(round(p_i.get_y() / p_i.get_x(), 5))
                if m !=0:
                    aux_fun_p = Function(m * Symbol('x'))
                else:
                    aux_fun_p = Function(0.0)
                if isinstance(fun, Function):
                    intersect = fun_intersect(fun, aux_fun_p)

                elif isinstance(fun, FunctionPoints):
                    intersect = fun_and_point(aux_fun_p, fun)

                if len(intersect) != 0:
                    for i in intersect:
                        # y_i = fun.eval(i)
                        if p_i.get_x() - gas < i < p_i.get_x() + gas:
                            continue
                        if p_i.get_x() < 0 and (i - p_i.get_x() > 0) \
                                or p_i.get_x() > 0 and (i - p_i.get_x() < 0):
                            exclude.append(p_i)
                            break

    out_aux = list(set(points) - set(exclude))
    out_aux.sort(key=lambda x: x.get_x())
    return out_aux


def get_centroid(points: list[IPoint]):
    x, y = 0, 0
    for point in points:
        x = x + point.get_x()
        y = y + point.get_y()
    return [x / len(points), y / len(points)]

@gui_utils.time_execution
def intersect_functions(fun_array: list, order=True) -> list[IPoint]:
    out_array = []
    # Realiza una intersección de la combinación de todas las funciones
    for fun in fun_array:
        # Define los extremos del sub recorrido
        start = fun_array.index(fun) + 1
        end = len(fun_array)
        # Ciclo para interceptar a la función actual fun con las funciones adelante en el arreglo
        for i in range(start, end):
            # Verifica que fun sea Function
            if isinstance(fun, Function):

                # Verifica que la función i-ésima sea Function para emplear fun_intersection
                if isinstance(fun_array[i], Function):
                    intersect = fun_intersect(fun, fun_array[i])
                    for x_i in intersect:
                        if fun.eval(x_i) is None and fun_array[i].eval(x_i) is None:
                            continue
                        else:
                            fun_eval = fun_array[i].eval(x_i) if fun.eval(x_i) is None else fun.eval(x_i)
                            out_array.append(IPoint(x_i, round(fun_eval, 4), fun, fun_array[i]))

                elif isinstance(fun_array[i], FunctionPoints):
                    intersect = fun_and_point(fun, fun_array[i])
                    for x_i in intersect:
                        out_array.append(IPoint(x_i, round(fun.eval(x_i), 4), fun, fun_array[i]))

            # Verifica que la función i-ésima sea FunctionPoints para emplear fun_and_points
            elif isinstance(fun, FunctionPoints):
                if isinstance(fun_array[i], Function):
                    intersect = fun_and_point(fun_array[i], fun)
                    for x_i in intersect:
                        out_array.append(IPoint(x_i, round(float(fun.eval(x_i)), 4), fun, fun_array[i]))
                #elif isinstance(fun_array[i], FunctionPoints):
                #    raise TypeError('There is no support for the intersection between two FunctionPoints.')
    if order:
        out_array.sort(key=lambda x: x.get_x())
    return out_array

@gui_utils.time_execution
def run_contour(points: list[IPoint], sentido=1, max_iters=100):
    ordened = []
    centroid = get_centroid(points)
    i = 0
    j = 1
    iters = 0
    while not len(ordened) == len(points):
        flag = True
        p_i = points[i]
        # Vector punto -> centroide
        pc_v = [centroid[0] - p_i.get_x(), centroid[1] - p_i.get_y()]
        while flag and iters < max_iters:
            if iters == max_iters:
                break
            p_j = points[j]
            # Vector punto_i -> punto_i+1
            pp1_v = [p_j.get_x() - p_i.get_x(), p_j.get_y() - p_i.get_y()]
            if p_i.is_connect(p_j) and p_i is not p_j:
                pv = float(pp1_v[0] * pc_v[1] - pp1_v[1] * pc_v[0])
                pv = pv / abs(pv)
                if pv - sentido == 0:
                    flag = False
                    i = j
                    ordened.append(p_i)
            j += 1
            if j > len(points) - 1:
                j = 0
            iters += 1
    if iters < max_iters:
        return ordened
    else:
        return None


def make_polygon(points: list[IPoint], sentido=1, step=20):
    polygon = []
    for i in range(0, len(points)):
        p_1 = points[i]
        if i + 1 > len(points) - 1:
            p_2 = points[0]
        else:
            p_2 = points[i + 1]

        if p_1.is_connect(p_2):
            link = p_1.link(p_2, sentido)
            x_array = np.linspace(p_1.get_x(), p_2.get_x(), num=step)
            for x_i in x_array:
                polygon.append((x_i, link.eval(x_i)))
    return polygon
