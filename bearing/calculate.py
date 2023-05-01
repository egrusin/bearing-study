__all__ = ['DrawData', 'DrawCoords', 'CalcData']


class DrawData:
    """Класс для рассчета недостающих параметров подшипника"""
    def __init__(self, data: dict) -> None:
        """Инициализатор данных класса
        :param data: dict - Словарь с имеющимися данными о подшипнике"""
        self.base_data = data
        self.data = dict.fromkeys(self.base_data, 0)

    def __mul__(self, other):
        """Метод для пропорционального увеличения параметров подшипника"""
        for i in self.data:
            self.data[i] *= other

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = float(value)


class CalcData:
    """Класс для расчета долговечности подшипника"""
    def __init__(self, data: dict) -> None:
        self.base_data = data
        self.data = dict.fromkeys(self.base_data, 0)

    def get_P(self):
        """Метод для расчета динамической нагрузки"""
        X = float(self.data.get('X'))
        V = float(self.data.get('V'))
        Fr = float(self.data.get('Fr'))
        Y = float(self.data.get('Y'))
        Fa = float(self.data.get('Fa'))
        Kb = float(self.data.get('k_t'))
        KT = float(self.data.get('k_t'))
        return round((X * V * Fr + Y * Fa) * Kb * KT, 4)

    def get_L(self):
        """Метод для расчета долговечности"""
        C = float(self.data.get('C'))
        p = float(self.data.get('p'))
        P = float(self.get_P())
        return round((C / P) ** p, 6)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value


class DrawCoords:
    """Класс для рассчета координат ключевых точек чертежа"""
    def __init__(self, data: DrawData, field_coords: tuple = (5, 5), field_size: tuple = (390, 590)) -> None:
        """Инициализируем размеры подшипника и поля для чертежа"""
        self.data = data
        self.field_coords = field_coords
        self.field_size = field_size

    def add_params(self):
        """Метод для расчета дополнительных параметров подшипника"""
        self['S'] = 0.15 * (self.data['D'] - self.data['d'])
        self['Dw'] = 0.32 * (self.data['D'] - self.data['d'])
        self['d1'] = 0.5 * (self.data['D'] + self.data['d'])

    def resize_data(self):
        """Метод для пропорционального увеличения параметров data"""
        k = min((self.field_size[0] - 20) // float(self.data['B']), (self.field_size[1] - 50) // float(self.data['D']))
        self.data * k

    def get_center(self):
        """Метод для получения координат x и y центра чертежа"""
        x = self.field_coords[0] + self.field_size[0] // 2
        y = self.field_coords[1] + self.field_size[1] // 2
        return x, y

    def get_inner_cilinder(self):
        """Метод для получения координат внутренней полости подшипника"""
        cent = self.get_center()
        x1 = cent[0] - 0.5 * self['B'] + self['r']                   # Левый верхний
        y1 = cent[1] - self['d'] // 2
        x2 = cent[0] + 0.5 * self['B'] - self['r']                   # Правый верхний
        y2 = y1
        x3 = cent[0] + 0.5 * self['B'] - self['r']                   # Правый нижний
        y3 = cent[1] + (self['d'] - self['d'] // 2)
        x4 = x1                                                      # Левый нижний
        y4 = y3
        return x1, y1, x2, y2, x3, y3, x4, y4

    def get_big_cilinder(self):
        """Метод для получения координат внутреннего цилиндра, условного статора"""
        cent = self.get_center()
        x1 = cent[0] - 0.5 * self['B']                               # Левый верхний
        y1 = cent[1] - self['d'] // 2 - self['S']
        x2 = cent[0] + 0.5 * self['B']                               # Правый верхний
        y2 = y1
        x3 = cent[0] + 0.5 * self['B']                               # Правый нижний
        y3 = cent[1] + (self['d'] - self['d'] // 2) + self['S']
        x4 = x1                                                      # Левый нижний
        y4 = y3
        return x1, y1, x2, y2, x3, y3, x4, y4

    def get_outer_polygon(self):
        """Метод для получения координат внешнего контура чертежа"""
        cent = self.get_center()
        x1 = cent[0] - 0.5 * self['B'] + self['r']
        y1 = cent[1] - self['D'] // 2
        x2 = cent[0] + 0.5 * self['B'] - self['r']
        y2 = y1
        x3 = cent[0] + 0.5 * self['B']
        y3 = y1 + self['r']
        x4 = x3
        y4 = cent[1] + self['D'] // 2 - self['r']
        x5 = x2
        y5 = cent[1] + self['D'] // 2
        x6 = x1
        y6 = y5
        x7 = cent[0] - 0.5 * self['B']
        y7 = y4
        x8 = x7
        y8 = y3
        return x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8

    def get_upinner_lines(self):
        """Метод для получения координат внутренних линий верхней части условного ротора"""
        cent = self.get_center()
        if self['S'] >= self['r']:
            x1 = cent[0] - 0.5 * self['B']
        else:
            x1 = cent[0] - 0.5 * self['B'] + (self['r'] - self['S'])
        y1 = cent[1] - self['D'] // 2 + self['S']
        x2 = cent[0]
        y2 = y1
        if 0.5 * self['S'] >= self['r']:
            x3 = cent[0] + 0.5 * self['B']
        else:
            x3 = cent[0] + 0.5 * self['B'] - (self['r'] - 0.5 * self['S'])
        y3 = cent[1] - self['D'] // 2 + 0.5 * self['S']
        x4 = cent[0] + 0.15 * self['B']
        y4 = cent[1] - 0.5 * self['d1'] - (self['Dw'] ** 2 / 4 - (0.15 * self['B']) ** 2) ** 0.5
        return x1, y1, x2, y2, x3, y3, x4, y4

    def get_downinner_lines(self):
        """Метод для получения координат внутренних линий нижней части условного ротора"""
        cent = self.get_center()
        if self['S'] >= self['r']:
            x1 = cent[0] - 0.5 * self['B']
        else:
            x1 = cent[0] - 0.5 * self['B'] + (self['r'] - self['S'])
        y1 = cent[1] + self['D'] // 2 - self['S']
        x2 = cent[0]
        y2 = y1
        if 0.5 * self['S'] >= self['r']:
            x3 = cent[0] + 0.5 * self['B']
        else:
            x3 = cent[0] + 0.5 * self['B'] - (self['r'] - 0.5 * self['S'])
        y3 = cent[1] + self['D'] // 2 - 0.5 * self['S']
        x4 = cent[0] + 0.15 * self['B']
        y4 = cent[1] + 0.5 * self['d1'] + (self['Dw'] ** 2 / 4 - (0.15 * self['B']) ** 2) ** 0.5
        return x1, y1, x2, y2, x3, y3, x4, y4

    def get_upcircle_params(self):
        """Метод для получения координат верхнего подшипника"""
        cent = self.get_center()
        x = cent[0]
        y = cent[1] - 0.5 * self['d1']
        r = 0.5 * self['Dw']
        return x - r, y - r, x + r, y + r

    def get_downcircle_params(self):
        """Метод для получения координат нижнего подшипника"""
        cent = self.get_center()
        x = cent[0]
        y = cent[1] + 0.5 * self['d1']
        r = 0.5 * self['Dw']
        return x - r, y - r, x + r, y + r

    def fill_up_stator(self, space=10):
        """Метод для получения координат штрихующих линий верхней части статора"""
        cent = self.get_center()
        left_up_x = cent[0] - 0.5 * self['B']
        left_up_y = cent[1] - self['d'] // 2 - self['S']
        right_up_x = cent[0] + 0.5 * self['B']
        right_up_y = left_up_y
        ans = []
        for i in range(0, int(self['B'] + self['S'] - self['r']), space):
            if i > self['B']:
                x1 = right_up_x
                y1 = right_up_y + i - self['B']
            else:
                x1 = left_up_x + i
                y1 = left_up_y
            if self['S'] - self['r'] < i < self['S'] + self['r']:
                x2 = left_up_x + (i - (self['S'] - self['r'])) / 2
                y2 = left_up_y + self['S'] - self['r'] + (i - (self['S'] - self['r'])) / 2
            elif i < self['S'] - self['r']:
                x2 = left_up_x
                y2 = left_up_y + i
            else:
                x2 = left_up_x + i - self['S']
                y2 = left_up_y + self['S']
            ans.append((x1, y1, x2, y2))
        return ans

    def fill_down_stator(self, space=10):
        """Метод для получения координат штрихующих линий нижней части статора"""
        cent = self.get_center()
        left_up_x = cent[0] - 0.5 * self['B']
        left_up_y = cent[1] + self['d'] // 2
        right_up_x = cent[0] + 0.5 * self['B']
        right_up_y = left_up_y
        start = int(self['r']) if self['r'] - int(self['r']) < 0.5 else int(self['r']) + 1
        ans = []
        for i in range(start, int(self['B'] + self['S']), space):
            if self['B'] - self['r'] < i < self['B'] + self['r']:
                x1 = right_up_x - self['r'] + (i - (self['B'] - self['r'])) / 2
                y1 = left_up_y + (i - (self['B'] - self['r'])) / 2
            elif i < self['B'] - self['r']:
                x1 = left_up_x + i
                y1 = left_up_y
            else:
                x1 = right_up_x
                y1 = right_up_y + i - self['B']
            if i < self['S']:
                x2 = left_up_x
                y2 = left_up_y + i
            else:
                x2 = left_up_x + i - self['S']
                y2 = left_up_y + self['S']
            ans.append((x1, y1, x2, y2))
        return ans

    def __getitem__(self, item):
        return float(self.data[item])

    def __setitem__(self, key, value):
        self.data[key] = float(value)
