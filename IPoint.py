import math

from Function import Function
from FunctionPoints import FunctionPoints


class IPoint:
    def __init__(self, x: float, y: float, f_1, f_2):
        if not (isinstance(f_1, Function) or isinstance(f_1, FunctionPoints)):
            raise AttributeError('You must insert as parameter an instance of Function or FunctionPoints.')
        if not (isinstance(f_2, Function) or isinstance(f_2, FunctionPoints)):
            raise AttributeError('You must insert as parameter an instance of Function or FunctionPoints.')
        self.__x = x
        self.__y = y
        self.__f_1 = f_1
        self.__f_2 = f_2
        self.__after_point()
        self.__before_point()

    def __str__(self):
        return f'(x, y) = ({self.__x}, {self.__y})'

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_xy(self):
        return [self.__x, self.__y]

    def get_f_1(self):
        return self.__f_1

    def get_f_2(self):
        return self.__f_2

    def major_before(self):
        return self.__major_b

    def minor_before(self):
        return self.__minor_b

    def major_after(self):
        return self.__major_a

    def minor_after(self):
        return self.__minor_a

    def __after_point(self):
        f_1_a = self.__f_1.eval(self.__x + 0.1)
        f_2_a = self.__f_2.eval(self.__x + 0.1)
        # Comprueba si las dos funciones NO EXISTEN después del punto para retornar None.
        if (f_1_a is None or f_1_a == 'Value out of range.') and (f_2_a is None or f_2_a == 'Value out of range.'):
            self.__minor_a = None
            self.__major_a = None
        # Comprueba si f_1 no existe pero f_2 si después del punto para guardar como mayor y menor a f_2
        elif (f_1_a is None or f_1_a == 'Value out of range.') and \
                not (f_2_a is None or f_2_a == 'Value out of range.'):
            self.__minor_a = self.__major_a = self.__f_2
        # Comprueba si f_2 no existe pero f_1 si después del punto para guardar como mayor y menor a f_1
        elif not (f_1_a is None or f_1_a == 'Value out of range.') \
                and (f_2_a is None or f_2_a == 'Value out of range.'):
            self.__minor_a = self.__major_a = self.__f_1
        # En este caso ambas funciones existen después del punto. Comprueba quien es mayor después.
        elif f_1_a >= f_2_a:
            self.__major_a = self.__f_1
            self.__minor_a = self.__f_2
        else:
            self.__major_a = self.__f_2
            self.__minor_a = self.__f_1

    def __before_point(self):
        f_1_b = self.__f_1.eval(self.__x - 0.1)
        f_2_b = self.__f_2.eval(self.__x - 0.1)
        # Comprueba si las dos funciones NO EXISTEN antes del punto para guardar None.
        if (f_1_b is None or f_1_b == 'Value out of range.') and (f_2_b is None or f_2_b == 'Value out of range.'):
            self.__minor_b = None
            self.__major_b = None
        # Comprueba si f_1 no existe pero f_2 si antes del punto para guardar como mayor y menor a f_2
        elif (f_1_b is None or f_1_b == 'Value out of range.') and \
                not (f_2_b is None or f_2_b == 'Value out of range.'):
            self.__minor_b = self.__major_b = self.__f_2
        # Comprueba si f_2 no existe pero f_1 si antes del punto para guardar como mayor y menor a f_1
        elif not (f_1_b is None or f_1_b == 'Value out of range.') \
                and (f_2_b is None or f_2_b == 'Value out of range.'):
            self.__minor_b = self.__major_b = self.__f_1
        # En este caso ambas funciones existen antes del punto. Comprueba quien es mayor y menor antes.
        elif f_1_b >= f_2_b:
            self.__major_b = self.__f_1
            self.__minor_b = self.__f_2
        else:
            self.__major_b = self.__f_2
            self.__minor_b = self.__f_1

    def distance(self, p_2):
        if not isinstance(p_2, IPoint):
            raise AttributeError('The second point to measure distance should be an instance of IPoint.')
        return math.sqrt((self.__x - p_2.get_x())**2 + (self.__y-p_2.get_y())**2)

    def get_vector(self, p_2):
        if not isinstance(p_2, IPoint):
            raise AttributeError('The second point to create a vector must be an instance of IPoint.')
        return [p_2.get_x() - self.__x, p_2.get_y() - self.__y]

    def is_connect(self, p_2):
        if self.get_f_1() == p_2.get_f_1() or self.get_f_1() == p_2.get_f_2():
            return True
        elif self.get_f_2() == p_2.get_f_1() or self.get_f_2() == p_2.get_f_2():
            return True
        else:
            return False

    def link(self, p_2, sentido):
        if (self.get_f_1() == p_2.get_f_1() or self.get_f_1() == p_2.get_f_2()) and (self.get_f_2() == p_2.get_f_1() or self.get_f_2() == p_2.get_f_2()):
            if sentido == -1:
                return self.minor_after()
            elif sentido == 1:
                return self.minor_before()
        elif self.get_f_1() == p_2.get_f_1() or self.get_f_1() == p_2.get_f_2():
            return self.get_f_1()
        elif self.get_f_2() == p_2.get_f_1() or self.get_f_2() == p_2.get_f_2():
            return self.get_f_2()
        else:
            return None