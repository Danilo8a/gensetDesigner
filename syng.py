import cmath
import math
from PyQt5 import QtCore
from numpy import deg2rad, rad2deg
from sympy import Symbol, sqrt, nsolve, sin
from Function import Function
from FunctionPoints import FunctionPoints
import numpy as np


# Clase abstracta para definir las funciones básicas de los generadores síncronos
class AbstractGen(QtCore.QObject):
    mess = QtCore.pyqtSignal(str)

    def get_electric_parameters(self) -> dict:
        pass

    def get_per_units_parameters(self):
        pass

    def get_load_angle(self, x, y):
        pass

    def get_induced_voltage(self, x, y):
        pass

    def get_math_model(self):
        pass

    def get_width(self):
        pass

    def get_only_functions(self):
        pass

    def _generate_model(self):
        pass


# Clase para definir a los generadores síncronos de polos salientes
class CylindricalGen(AbstractGen):

    def __init__(self, sn, vn, fp, xs, p_motriz, seg_min, seg_prac, ef=None, per_units=True):

        # Si los valores no están en PU, los convierte a PU
        super().__init__()
        if not per_units:
            z_b = (vn ** 2) / sn
            vn, sn, xs, p_motriz = 1, 1, xs / z_b, p_motriz / vn

        self._values = list()
        self.s_nom_pu = sn
        self.v_nom_pu = vn
        self.fp = fp
        self.xs_pu = xs
        self.p_motriz_pu = p_motriz
        self.tension_max_campo = ef
        self.porcentaje_s_min = seg_min
        self.porcentaje_seg_prac = seg_prac

        # Corrección del porcentaje de seguridad mínima
        if self.porcentaje_s_min > 0.1:
            self.porcentaje_s_min = 0.1
        if self.porcentaje_s_min < 0.02:
            self.porcentaje_s_min = 1.0

        # Corrección del porcentaje de seguridad práctica
        if self.porcentaje_seg_prac > 0.1:
            self.porcentaje_seg_prac = 0.1
        if self.porcentaje_seg_prac < 0.02:
            self.porcentaje_seg_prac = 0.02

        # Corrección del valor de potencia motriz
        if self.p_motriz_pu == 0:
            self.p_motriz_pu = self.s_nom_pu

        # Cálculo de la tensión máxima de campo
        if self.tension_max_campo is None:
            self.tension_max_campo = cmath.rect(self.v_nom_pu, 0) + cmath.rect(self.xs_pu, cmath.pi / 2) * cmath.rect(1,
                                                                                                                      -self.fp)
            self.tension_max_campo = abs(self.tension_max_campo)

        self._generate_model()

    # Devuelve un vector con los parámetros del generador en PU
    def get_per_units_parameters(self):
        return [
            self.s_nom_pu,
            self.v_nom_pu,
            self.fp,
            self.xs_pu,
            self.p_motriz_pu,
            self.tension_max_campo,
            self.porcentaje_s_min,
            self.porcentaje_seg_prac
        ]

    # Devuelve el valor del ángulo de carga
    def get_load_angle(self, x, y):
        return math.atan(y / (x + (self.v_nom_pu ** 2) / self.xs_pu))

    # Devuelve el valor de la tensión inducida en PU
    def get_induced_voltage(self, x, y):
        a = (self.v_nom_pu ** 2 / self.xs_pu) + x
        b = self.xs_pu / self.v_nom_pu
        return b * math.sqrt(a ** 2 + y ** 2)

    # Devuelve el radio de la circunferencia de exitación
    def get_radio(self):
        return self.tension_max_campo * self.v_nom_pu / self.xs_pu

    # Devuelve el radio de la circunferencia del límite de exitación
    def get_radio_min(self):
        return self.get_radio() * (0.1 + self.porcentaje_s_min)

    # Devuelve el centro de la cirunferencia de exitación
    def get_center(self):
        return - self.v_nom_pu ** 2 / self.xs_pu

    # Genera los modelos con las ecuaciones que describen a los límites de operación
    def _generate_model(self):

        self.mess.emit('Calculando parámetros en PU.')
        self._x = Symbol('x')
        # Límite de armadura
        self._armor_limit = Function(sqrt(self.v_nom_pu ** 2 - self._x ** 2))
        self._armor_limit_dom = list(
            map(float, list(np.linspace(-self.v_nom_pu + 0.00001, self.v_nom_pu - 0.00001, 500))))

        # Límite de exitación
        r = self.get_radio()
        h = self.get_center()
        self._excitation_limit = Function(sqrt(r ** 2 - (self._x - h) ** 2))
        self._excitation_limit_dom = list(map(float, list(np.linspace(h, h + r - 0.00001, 50))))

        # Potencia mecánica
        self._mechanical_power = Function(self.p_motriz_pu)

        # Límite de exitación mínima
        r_m = self.get_radio_min()
        self._min_exc_limit = Function(sqrt(r_m ** 2 - (self._x - h) ** 2))
        self._min_exc_limit_dom = list(map(float, list(np.linspace(h - 0.00001, h + r_m - 0.00001, 30))))

        # Límite práctico
        values_x = []
        values_y = []
        rango = [z / 10 for z in range(10, 0, -1)]
        for i in rango:
            r_i = r * i
            y = (r * i) - (r * self.porcentaje_seg_prac)
            x = sqrt(r_i ** 2 - y ** 2) + h
            values_x.append(float(x))
            values_y.append(float(y))
        self._practical_limit = FunctionPoints(values_x, values_y, grid=500)
        self._practical_limit_dom = list(
            map(float, list(np.linspace(values_x[0] - 0.00000001, values_x[-1] + 0.00000001, 25))))

    # Devuelve un diccionario con las ecuaciones que describen a los límites de operación
    def get_math_model(self):
        return {
            "armor": [self._armor_limit, self._armor_limit_dom],
            "excitation": [self._excitation_limit, self._excitation_limit_dom],
            "mechanical": [self._mechanical_power, list(self.get_width())],
            "min_exc": [self._min_exc_limit, self._min_exc_limit_dom],
            "practical": [self._practical_limit, self._practical_limit_dom]
        }

    # Calcula el ancho para la figura
    def get_width(self):
        x_min = min(self._armor_limit_dom[0], self._practical_limit_dom[0], self._min_exc_limit_dom[0],
                    self._excitation_limit_dom[0]) - 0.2
        x_max = max(self._armor_limit_dom[-1], self._practical_limit_dom[-1], self._min_exc_limit_dom[-1],
                    self._excitation_limit_dom[-1]) + 0.2
        return [x_min, x_max]

    def get_only_functions(self):
        return [
            self._armor_limit,
            self._excitation_limit,
            self._mechanical_power,
            self._min_exc_limit,
            self._practical_limit
        ]

    def get_electric_parameters(self) -> dict:
        return {
            "S: ": self.s_nom_pu,
            "V: ": self.v_nom_pu,
            "Fp: ": self.fp,
            "Xs: ": self.xs_pu,
            "P: ": self.p_motriz_pu,
            "Ef: ": self.tension_max_campo,
            "Seg. min.: ": self.porcentaje_s_min,
            "Seg. prac. ": self.porcentaje_seg_prac
        }


class SalientGen(AbstractGen):

    def __init__(self, sn, vn, fp, xd, xq, p_motriz, seg_min, seg_prac, ef=None, per_units=True):
        super().__init__()
        if not per_units:
            z_b = (vn ** 2) / sn
            vn, sn, xq, xd, p_motriz = 1, 1, xq / z_b, xd / z_b, p_motriz / vn

        self.s_nom_pu = sn
        self.v_nom_pu = vn
        self.fp = fp
        self.xd_pu = xd
        self.xq_pu = xq
        self.p_motriz_pu = p_motriz
        self.tension_max_campo = ef
        self.porcentaje_s_min = seg_min
        self.porcentaje_seg_prac = seg_prac

        # Corrección del porcentaje de seguridad mínima
        if self.porcentaje_s_min > 0.1:
            self.porcentaje_s_min = 0.1
        if self.porcentaje_s_min < 0.02:
            self.porcentaje_s_min = 1.0

        # Corrección del porcentaje de seguridad práctica
        if self.porcentaje_seg_prac > 0.1:
            self.porcentaje_seg_prac = 0.1
        if self.porcentaje_seg_prac < 0.02:
            self.porcentaje_seg_prac = 0.02

        # Corrección del valor de potencia motriz
        if self.p_motriz_pu == 0:
            self.p_motriz_pu = self.s_nom_pu

        # Cálculo de la tensión máxima de campo
        if self.tension_max_campo is None:
            self.tension_max_campo = cmath.rect(self.v_nom_pu, 0) + cmath.rect(self.xq_pu, cmath.pi / 2) * cmath.rect(1, -math.acos(self.fp))
            i_d = abs(cmath.sin(math.acos(self.fp) + cmath.phase(self.tension_max_campo)))
            self.tension_max_campo = abs(self.tension_max_campo) + (self.xd_pu - self.xq_pu) * i_d
        else:
            self.tension_max_campo = ef

        self._generate_model()

    def get_delta_max(self, e_f):
        k_1 = self.v_nom_pu ** 2 * (1 / self.xq_pu - 1 / self.xd_pu)
        k_2 = self.v_nom_pu * e_f / self.xd_pu
        q = -(k_2 / (4 * k_1)) + sqrt(k_2 ** 2 + 8 * k_1 ** 2) / (4 * k_1)
        return float(math.acos(q))

    # Sin uso, por ahora
    def get_x_y(self, delta):
        a = 1 + math.tan(delta) ** 2
        b = self._o_p + self._o_pp + 2 * self._o_pp * math.tan(delta) ** 2
        c = self._o_pp ** 2 * math.tan(delta) ** 2 + self._o_p * self._o_pp
        x = - b / (2 * a) + sqrt(b ** 2 - 4 * a * c) / (2 * a)
        y = math.tan(delta) * (x + self._o_pp)

        return float(x), float(y)

    # Sin uso, por ahora
    def get_p_q(self, x, y, delta, e_f):
        p = (sqrt(x ** 2 + y ** 2) + e_f * self.v_nom_pu / self.s_nom_pu) * math.sin(delta)
        q = (sqrt(x ** 2 + y ** 2) + e_f * self.v_nom_pu / self.s_nom_pu) * math.cos(delta) - self._o_pp

        return float(q), float(p)

    def get_p_q_e(self, delta, e_f):
        k_2 = self.v_nom_pu ** 2 * (1 / self.xq_pu - 1 / self.xd_pu)
        k_1 = e_f * self.v_nom_pu / self.xd_pu
        r = k_1 + k_2 * math.cos(delta)
        p = r * math.sin(delta)
        q = r * math.cos(delta) - self._o_pp
        return q, p

    def get_delta_p(self, p_i, e_f, delta):
        k_1 = (self.v_nom_pu ** 2 / 2) * (1 / self.xq_pu - 1 / self.xd_pu)
        k_2 = e_f * self.v_nom_pu / self.xd_pu
        delta_p = nsolve(p_i - self.porcentaje_seg_prac - k_1 * sin(2 * self._x) - k_2 * sin(self._x), (0, delta),
                         solver='bisect')
        return delta_p

    def _generate_model(self):
        self._x = Symbol('x')
        aux_flag = False
        # Potencia mecánica
        self._mechanical_power = Function(self.p_motriz_pu)

        # Límite de armadura
        self._armor_limit = Function(sqrt(self.v_nom_pu ** 2 - self._x ** 2))
        self._armor_limit_dom = list(
            map(float, list(np.linspace(-self.v_nom_pu + 0.0001, self.v_nom_pu - 0.0001, 500))))

        # Cálculos para el resto de límites
        self._o_p = self.v_nom_pu ** 2 / self.xd_pu
        self._o_pp = self._o_p + self.v_nom_pu ** 2 * (1 / self.xq_pu - 1 / self.xd_pu)
        self._h_o = (self._o_pp + self._o_p) / 2
        self._r_o = (self._o_pp - self._o_p) / 2
        self._d_e_f_max = self.tension_max_campo * self.v_nom_pu / self.xd_pu

        # Límite de exitación
        exitacion_x = []
        exitacion_y = []
        for delta in np.linspace(deg2rad(0.0), math.pi / 2 - 0.001, 50):
            delta = float(delta)
            q, p = self.get_p_q_e(delta, self.tension_max_campo)
            exitacion_x.append(q)
            exitacion_y.append(p)
        self._excitation_limit = FunctionPoints(exitacion_x, exitacion_y)
        self._excitation_limit_dom = self._excitation_limit.get_x()

        # Límite de excitation mínima
        radio_min = self._r_o + self._d_e_f_max * self.porcentaje_s_min
        self._excitation_min_limit = Function(sqrt(radio_min ** 2 - (self._x + self._h_o) ** 2))
        self._excitation_min_limit_dom = list(
            map(float, list(np.linspace(-self._h_o - radio_min + 0.0001, -self._h_o + radio_min - 0.0001, 500))))

        # Límite circulito
        self._excitation_min = Function(sqrt(self._r_o ** 2 - (self._x + self._h_o) ** 2))
        self._excitation_min_dom = list(
            map(float, list(np.linspace(-self._h_o - self._r_o + 0.0001, -self._h_o + self._r_o - 0.0001, 500))))

        # Límites de estabilidad práctica y teórica
        e_t_x = []
        e_t_y = []
        e_p_x = []
        e_p_y = []

        for i in np.linspace(1, 0, 40):
            i = float(i)

            # Estabilidad teórica
            e_i = self.tension_max_campo * i
            delta_max = self.get_delta_max(e_i)
            q, p = self.get_p_q_e(delta_max, e_i)
            e_t_x.append(q)
            e_t_y.append(p)

            # Estabilidad práctica
            if p >= self.porcentaje_seg_prac:
                delta_p = self.get_delta_p(p, e_i, delta_max)
                q, p = self.get_p_q_e(delta_p, e_i)
                e_p_x.append(q)
                e_p_y.append(p)
            else:
                aux_flag = True
        if aux_flag:
            h = nsolve((e_p_x[-1] - self._x) ** 2 / e_p_y[-1] - (e_p_x[-2] - self._x) ** 2 / e_p_y[-2],
                       (-self._h_o, e_p_x[-1]), solver='bisect')
            h = float(h)
            # Cuadrático parábola con vértice en (h, k) = (o_p, 0)
            l_r = (e_p_x[-1] - h) ** 2 / e_p_y[-1]
            aux_x = list(map(float, list(np.linspace(h, e_p_x[-1], 20, endpoint=False))))
            aux_y = list(map(lambda x: (1 / l_r) * (x - h) ** 2, aux_x))
            e_p_x += aux_x
            e_p_y += aux_y

        self._practical_limit = FunctionPoints(e_p_x, e_p_y)
        self._practical_limit_dom = self._practical_limit.get_x()
        self._teorical_limit = FunctionPoints(e_t_x, e_t_y)
        self._teorical_limit_dom = self._teorical_limit.get_x()

    def get_math_model(self):
        return {
            "armor": [self._armor_limit, self._armor_limit_dom],
            "excitation": [self._excitation_limit, self._excitation_limit_dom],
            "mechanical": [self._mechanical_power, list(self.get_width())],
            "teorical": [self._teorical_limit, self._teorical_limit_dom],
            "practical": [self._practical_limit, self._practical_limit_dom],
            "exitacion_min": [self._excitation_min_limit, self._excitation_min_limit_dom],
            "exitación_min_punteado": [self._excitation_min, self._excitation_min_dom]
        }

    # Calcula el ancho para la figura
    def get_width(self):
        x_min = min(self._armor_limit_dom[0], self._practical_limit_dom[0], self._teorical_limit_dom[0],
                    self._excitation_limit_dom[0])
        x_max = max(self._armor_limit_dom[-1], self._practical_limit_dom[-1], self._teorical_limit_dom[-1],
                    self._excitation_limit_dom[-1])
        return [x_min, x_max]

    # Retorna a los límites de la máquina sin los dominios
    def get_only_functions(self):
        return [
            self._armor_limit,
            self._excitation_limit,
            self._mechanical_power,
            self._practical_limit,
            self._excitation_min_limit
        ]

    def get_load_angle(self, x, y):
        return math.atan(abs(y) / (x + self._o_pp))

    def get_induced_voltage(self, x, y):
        # La magnitud del voltaje inducido se calcula mediante la ley del coseno
        # el lado a, corresponde con la potencia inducida
        # el lado b, corresponde con la potencia reactiva de la máquina debido a x_d
        # el lado c, corresponde con la potencia aparente de armadura
        circulito = self._excitation_min
        m = y / (x + self._o_pp)
        x_aux = float(nsolve((m**2 + 1) * self._x**2 + 2 * (m**2 * self._o_pp + self._h_o) * self._x + m**2 * self._o_pp + self._h_o**2, (-round(self._o_pp, 2) + 0.01, -round(self._o_p, 2)), solver='bisect', verify=False))
        y_aux = circulito.eval(x_aux)
        d = math.sqrt((x_aux - x)**2 + (y_aux - y)**2)
        d = self.xd_pu * d
        return d

    def get_electric_parameters(self) -> dict:
        return {
            "S: ": self.s_nom_pu,
            "V: ": self.v_nom_pu,
            "Fp: ": self.fp,
            "Xd: ": self.xd_pu,
            "Xq: ": self.xq_pu,
            "P: ": self.p_motriz_pu,
            "Ef: ": self.tension_max_campo,
            "Seg. min.: ": self.porcentaje_s_min,
            "Seg. prac. ": self.porcentaje_seg_prac
        }
