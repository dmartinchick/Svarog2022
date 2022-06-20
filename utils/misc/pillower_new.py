"""Пакет работы с таблицами результатов ver2.0"""

from datetime import datetime

from PIL import Image, ImageFont, ImageDraw

from utils.misc.results_processing import CupResults, FestivalResult, HoldingResult


class ResultsTable:
    """Класс для работы с таблицами результатов"""

    def __init__(self, results_data):
        self.__background = 'data/img/results_new/background.jpg'
        self.img = Image.open(self.__background)
        self.canvas = ImageDraw.Draw(self.img)
        self.splitter = Splitter(self.img.size)

        self.title = Title(self.img, self.canvas, self.splitter)
        self.footer = Footer(self.img, self.canvas, self.splitter)
        self.table = Table(img=self.img,
                           canvas=self.canvas,
                           splitter=self.splitter,
                           results_data=results_data)

    def show_table(self):
        """Функция отображения таблицы"""

        self.img.show()


class Splitter:
    """Класс для раскройки таблицы на функциональные блоки"""

    def __init__(self, img_size):
        self.__img_size = img_size
        self.__title_size = (0, 0)
        self.__footer_size = (0, 0)
        self.__table_size = (0, 0)
        self.__cell_width = 0
        self.__header_height = 0
        self.__results_data_height = 0
        self.__row_name_width = 0

    def get_img_size(self) -> tuple:
        """Метод возвращает размер фона

        Returns:
            tuple: размер фона
        """
        return self.__img_size

    def set_title_size(self, width, height):
        """Метод устанавливает размер заголовка таблицы результатов

        Args:
            width (_type_): ширина заголовка
            height (_type_): высота заголовка
        """
        self.__title_size = (width, height)
        self.set_table_size()

    def get_title_size(self) -> tuple:
        """Метод возвращает размер заголовка таблицы результатов

        Returns:
            tuple: (ширина, высота) заголовка таблицы результатов
        """
        return self.__title_size

    def set_footer_size(self, width, height):
        """Метод устанавливает размер футтера таблицы результатов

        Args:
            width (_type_): ширина футера
            height (_type_): высота футера
        """
        self.__footer_size = (width, height)
        self.set_table_size()

    def get_footer_size(self) -> tuple:
        """Метод возвращает размер футера таблицы результатов

        Returns:
            tuple: (ширина, высота) футера таблицы результатов
        """
        return self.__footer_size

    def set_table_size(self, width=None):
        """Метод устанавливает размер таблицы с данными результатов

        Args:
            width (int or float, optional): ширина таблицы с данными. Defaults to None.
        """
        if width is None:
            self.__table_size = (
                self.get_img_size()[0],
                self.__img_size[1] - self.__title_size[1] - self.__footer_size[1]
            )
        else:
            self.__table_size = (
                width,
                self.__img_size[1] - self.__title_size[1] - self.__footer_size[1])

    def get_table_size(self):
        """Метод возвращает размер таблицы с данными результатов

        Returns:
            tuple: (ширина, высота) таблицыс данными результатов
        """
        return self.__table_size

    def set_cell_width(self, width):
        """Метод устанавливает ширину ячейки в таблице данных.

        Args:
            width (_type_): ширина ячейки
        """
        self.__cell_width = width

    def get_cell_width(self) -> int or float:
        """Метод возвращает ширину ячейки в таблице данных

        Returns:
            int or float: ширина ячейки
        """
        return self.__cell_width

    def set_header_height(self, height):
        """Метод устанавливает высоту заголовка таблицы результатов

        Args:
            height (int or float): высота заголовка
        """
        self.__header_height = height
        self.set_results_data_height()

    def get_header_height(self) -> int or float:
        """Метод возвращает высоту заголовка таблицы результатов

        Returns:
           int or float: высота заголовка таблицы результатов
        """
        return self.__header_height

    def set_results_data_height(self):
        """Метод вычисляет выосту таблицы данных
        """
        self.__results_data_height = self.__table_size[1] - self.__header_height

    def get_results_data_height(self) -> int or float:
        """Метод возвращает высоту таблицы данных

        Returns:
            int or float: высота таблицы
        """
        return self.__results_data_height

    def set_row_name_width(self, width):
        """Метод устанавливает ширину названия строк

        Args:
            width (_type_): ширина названия строк
        """
        self.__row_name_width = width

    def get_row_name_width(self) -> int or float:
        """Метод возвращает ширину названия строк

        Returns:
            int or float: ширина названия строк
        """

        return self.__row_name_width


class Area:
    """Класс для работы с размерами элементов таблицы результатов"""

    def __init__(self):
        self.__padding = (0, 0, 0, 0)
        self.__point_x0 = 0
        self.__point_y0 = 0
        self.__text_size = (0, 0)
        self.__size_x = 0
        self.__size_y = 0

    def set_padding(self, padding):
        """Метод устанавливает отсутупы элементов талицы

        Args:
            padding (tuple): (top, left, right, bottom) отступы элементов таблицы
        """
        self.__padding = padding

    def get_padding(self) -> tuple:
        """Метод возвращает отсутупы элементов таблицы

        Returns:
            tuple: отступ элементов таблицы
        """
        return self.__padding

    def set_point_x0(self, point_x0: int or float):
        """Метод устанавливает точку x0 элемента таблицы

        Args:
            point_x0 (int or float): точка x0
        """
        self.__point_x0 = point_x0

    def get_point_x0(self) -> int or float:
        """Метод возвращает точку x0 элемента таблицы

        Returns:
            int or float: точка x0
        """
        return self.__point_x0

    def set_point_y0(self, point_y0):
        """Метод устанавливает точку y0 элемента таблицы

        Args:
            point_y0 (int or float): точка y0
        """
        self.__point_y0 = point_y0

    def get_point_y0(self):
        """Метод возвращает точку y0 элемента таблицы

        Returns:
            int or float: точка y0
        """
        return self.__point_y0

    def set_point(self, point_x0, point_y0):
        """Метод устанавливает координаты точки x0, y0

        Args:
            point_x0 (_type_): точка x0
            point_y0 (_type_): точка y0
        """
        if point_x0 is None and point_y0 is None:
            self.__point_x0, self.__point_y0 = self.__point_x0, self.__point_y0
        elif point_x0 is not None and point_y0 is None:
            self.__point_x0, self.__point_y0 = point_x0, self.__point_y0
        elif point_x0 is None and point_y0 is not None:
            self.__point_x0, self.__point_y0 = self.__point_x0, point_y0
        else:
            self.__point_x0, self.__point_y0 = point_x0, point_y0

    def get_point(self):
        """МЕтод возвращает координаты x0, y0

        Returns:
           tuple: координаты точки x0y0
        """
        return self.__point_x0, self.__point_y0

    def set_text_size(self, text_size: tuple):
        """Метод устанавливает размер текста

        Args:
            text_size (tuple): размер текста
        """
        self.__text_size = text_size

    def get_text_size(self) -> tuple:
        """Метод возвращает размер текста

        Returns:
            tuple: (ширина, высота) размер текста
        """
        return self.__text_size

    def set_size(self, size_x=None, size_y=None):
        """Метод устанавливает размеры элемента

        Args:
            size_x (_type_, optional): ширина элемента. Defaults to None.
            size_y (_type_, optional): высота элемнта. Defaults to None.
        """
        if size_x is None and size_y is None:
            self.__size_x, self.__size_y = self.__size_x, self.__size_y
        elif size_x is not None and size_y is None:
            self.__size_x, self.__size_y = size_x, self.__size_y
        elif size_x is None and size_y is not None:
            self.__size_x, self.__size_y = self.__size_x, size_y
        else:
            self.__size_x, self.__size_y = size_x, size_y

    def get_size(self):
        """Метод возвращает размеры элемнта

        Returns:
            (tuple): (ширина, высота) элемента
        """
        return self.__size_x, self.__size_y

    @staticmethod
    def calculate_coord(point_x0, point_y0, size_x, size_y, text_size, anchor):
        """Метод для расчета координаты точки с которой будет начинаться текст

        Args:
            point_x0 (_type_): точка X0
            point_y0 (_type_): точка Y0
            size_x (_type_): ширина элемента
            size_y (_type_): высота элемента
            text_size (_type_): размер размещаемого текста
            anchor (_type_): якорь

        Returns:
            (tuple): (x, y) координаты точки с которой будет начинаться текст
        """
        anchor_to_coord = {
            'la': (point_x0,
                   point_y0),
            'ma': (point_x0 + size_x/2 - text_size[0]/2,
                   point_y0),
            'ra': (point_x0 + size_x - text_size[0],
                   point_y0),
            'lm': (point_x0,
                   point_y0 + size_y / 2 - text_size[1] / 2),
            'mm': (point_x0 + size_x / 2 - text_size[0] / 2,
                   point_y0 + size_y / 2 - text_size[1] / 2),
            'rm': (point_x0 + size_x - text_size[0],
                   point_y0 + size_y / 2 - text_size[1] / 2),
            'lb': (point_x0,
                   point_y0 + size_y - text_size[1]),
            'mb': (point_x0 + size_x / 2 - text_size[0] / 2,
                   point_y0 + size_y - text_size[1]),
            'rb': (point_x0 + size_x - text_size[0],
                   point_y0 + size_y - text_size[1])
        }
        return anchor_to_coord[anchor]


class Cell:
    """Класс для работы с элементами таблицы результатов"""

    def __init__(self, img, canvas, splitter):
        self.img = img
        self.area = Area()
        self.canvas = canvas
        self.splitter = splitter
        self.__text = ''
        self.__font_path = 'data/fonts/Montserrat-Regular.ttf'
        self.__font_size = 20
        self.__font = ImageFont.truetype(font=self.__font_path, size=self.__font_size)
        self.__fill = (255, 255, 255)
        self.__anchor = 'la'

    def set_font(self, font_path=None, font_size=None):
        """Метод для установки шрифта

        Args:
            font_path (_type_, optional): путь к шрифту. Defaults to None.
            font_size (_type_, optional): размер шрифта. Defaults to None.
        """
        if font_path is None and font_size is None:
            self.__font = ImageFont.truetype(self.__font_path, self.__font_size)
        elif font_path is not None and font_size is None:
            self.__font = ImageFont.truetype(font_path, self.__font_size)
        elif font_path is None and font_size is not None:
            self.__font = ImageFont.truetype(self.__font_path, font_size)
        else:
            self.__font = ImageFont.truetype(font_path, font_size)

    def get_font(self):
        """Метод возвращает шрифт

        Returns:
            ImageFont: Шрифт
        """
        return self.__font

    def set_text(self, text):
        """Метод устанавливает текст, который будет размещен в таблице результатов

        Args:
            text (_type_): текст
        """
        self.__text = text

    def get_text(self) -> str:
        """Метод возвращает текст, который будет размещен в таблице результатов

        Returns:
            str: текст
        """
        return self.__text

    def set_fill(self, fill):
        """Метод установки цвета заливки

        Args:
            fill (_type_): Заливка в формате (R, G, B), где RGB - числовые значения от 0 до 255
        """
        if fill is None:
            self.__fill = self.__fill
        else:
            self.__fill = fill

    def get_fill(self):
        """Get fill"""
        return self.__fill

    def set_anchor(self, anchor):
        """Set anchor"""
        if anchor is None:
            self.__anchor = self.__anchor
        else:
            self.__anchor = anchor

    def get_anchor(self):
        """get anchor"""
        return self.__anchor

    def set_point(self, point_x0=None, point_y0=None):
        """Метод установки точки начала ячейки"""
        self.area.set_point(point_x0, point_y0)

    def set_text_size(self):
        """Метод установки размера текста"""
        self.area.set_text_size(
            text_size=self.canvas.textsize(text=self.__text,
                                           font=self.__font)
        )

    def set_area_size(self):
        """Методо установки размера ячейки"""
        self.area.set_size(
            size_x=self.area.get_text_size()[0],
            size_y=self.area.get_text_size()[1]
        )

    def set_splitter_size(self):
        """Метод передачи размера в разделитель"""
        pass

    def draw_text(self,
                  text,
                  padding,
                  fill=None,
                  anchor=None,
                  font_path=None,
                  font_size=None,
                  ):
        """Метод печатает текст на фоон"""
        self.set_text(text)
        self.area.set_padding(padding)
        self.set_fill(fill)
        self.set_anchor(anchor)
        self.set_font(font_path, font_size)
        self.set_point()
        self.set_text_size()
        self.set_area_size()
        self.canvas.text(
            xy=self.area.calculate_coord(point_x0=self.area.get_point()[0],
                                         point_y0=self.area.get_point()[1],
                                         size_x=self.area.get_size()[0],
                                         size_y=self.area.get_size()[1],
                                         text_size=self.area.get_text_size(),
                                         anchor=self.__anchor),
            text=self.__text,
            font=self.__font,
            fill=self.__fill
        )
        self.set_splitter_size()


class Title(Cell):
    """Класс для работы с заголовком таблицы результатов

    Args:
        Cell (_type_): наследуемый клас для работы с элементами таблицы результатов
    """

    def set_point(self, point_x0=None, point_y0=None):
        self.area.set_point(
            point_x0=self.area.get_padding()[1],
            point_y0=self.area.get_padding()[0]
        )

    def set_area_size(self):
        self.area.set_size(
            size_x=(self.img.size[0] -
                    self.area.get_padding()[1] -
                    self.area.get_padding()[2]),
            size_y=self.area.get_text_size()[1]
        )

    def set_splitter_size(self):
        self.splitter.set_title_size(
            width=self.img.size[0],
            height=(self.area.get_padding()[0] +
                    self.area.get_text_size()[1] +
                    self.area.get_padding()[3])
        )


class Footer(Cell):
    """Класс для работы с футером таблицы результатов

    Args:
        Cell (_type_): наследуемый клас для работы с элементами таблицы результатов
    """

    def set_point(self, point_x0=None, point_y0=None):
        self.area.set_point(
            point_x0=self.area.get_padding()[1],
            point_y0=(self.img.size[1] -
                      self.area.get_text_size()[1] -
                      self.area.get_padding()[3])
        )

    def set_area_size(self):
        self.area.set_size(
            size_x=(self.img.size[0] -
                    self.area.get_padding()[1] -
                    self.area.get_padding()[2]),
            size_y=self.area.get_text_size()[1]
        )

    def set_splitter_size(self):
        self.splitter.set_footer_size(
            width=self.img.size[0],
            height=(self.area.get_padding()[0] +
                    self.area.get_text_size()[1] +
                    self.area.get_padding()[3])
        )


class Row(Cell):
    """Класс для работы со строками таблицы результатов

    Args:
        Cell (_type_): наследуемый клас для работы с элементами таблицы результатов
    """

    def __init__(self, img, canvas, splitter, results_data):
        super(Row, self).__init__(img, canvas, splitter)
        self.results_data = results_data
        self.set_settings()
        self.set_cell_width()

    def set_settings(self,
                     padding=(0, 0, 0, 0),
                     row_name_left_padding=0,
                     font_path=None,
                     font_size=None,
                     fill=(255, 255, 255),
                     anchor='la'):
        """Метод добавления настроек к строке"""
        self.area.set_padding(padding)
        self.set_point()
        self.area.__setattr__("row_name_left_padding", row_name_left_padding)
        self.set_font(font_path, font_size)
        self.set_fill(fill)
        self.set_anchor(anchor)

    def set_point(self, point_x0=None, point_y0=None):
        """Метод установки начальной точки с которой начинается строка"""
        self.area.set_point(
            point_x0=self.area.get_padding()[1],
            point_y0=self.splitter.get_title_size()[1]
        )

    def set_cell_width(self):
        """Метод установки размеров ячейки в строке"""

        self.splitter.set_cell_width((self.splitter.get_img_size()[0] -
                                      self.area.get_padding()[1] -
                                      self.splitter.get_row_name_width() -
                                      self.area.__getattribute__('row_name_left_padding') -
                                      self.area.get_padding()[2]) /
                                     (len(self.results_data[0].keys())-1))

    def set_area_size(self):
        """Метод установки размеров ячеек в строке"""
        self.area.set_size(
            size_x=((self.splitter.get_img_size[0] -
                    self.area.get_padding()[1] -
                    self.area.get_padding()[2] -
                    self.area.__getattribute__('row_name_left_padding') -
                    self.splitter.get_row_name_width) /
                    (len(self.results_data[0].keys())-1)),
            size_y=self.splitter.get_header_height()
        )

    def get_header_list(self):
        """Метод получения заголовков в таблице данных"""
        header_list = []
        for item in self.results_data[0].keys():
            header_list.append(item.replace(" ", "\n", 1))
        return header_list

    def get_keys(self):
        """get keys"""
        keys = []
        for column in self.results_data[0].keys():
            keys.append(column)
        return keys

    def get_steps(self) -> dict:
        """get steps
        TODO: del?"""
        pass

    def draw_table(self):
        """draw table
        TODO: del?"""
        pass


class Table:
    """Класс для создания и работы с таблицей результатов"""

    def __init__(self, img, canvas, splitter, results_data):
        self.results_data = results_data
        self.header = Header(img, canvas, splitter, self.results_data)
        self.table_data = TableData(img, canvas, splitter, self.results_data)

    def draw_table(self):
        """Метод печатает таблицу на фоне"""
        self.header.draw_header()
        self.table_data.draw_table()


class Header(Row):
    """Класс для работы с заголовками столбцов таблицы результатов

    Args:
        Row (_type_): наследуемый класс для работы со строками таблицы данных
    """

    def set_settings(self,
                     padding=(0, 0, 0, 0),
                     row_name_left_padding=0,
                     font_path=None,
                     font_size=None,
                     fill=(255, 255, 255),
                     anchor='la'):
        super(Header, self).set_settings(padding,
                                         row_name_left_padding,
                                         font_path,
                                         font_size,
                                         fill,
                                         anchor)
        self.set_header_height()
        self.set_cell_width()

    def set_point(self, point_x0=None, point_y0=None):
        self.area.set_point(
            point_x0=self.area.get_padding()[1],
            point_y0=self.splitter.get_title_size()[1]
        )

    def set_header_height(self):
        """Метод устанавливает выосту заголовка таблицы"""
        max_height = 0
        for item in self.results_data[0].keys():
            if self.canvas.textsize(item.replace(" ", "\n", 1), self.get_font())[1] > max_height:
                max_height = self.canvas.textsize(item.replace(" ", "\n", 1), self.get_font())[1]
        self.splitter.set_header_height(max_height)

    def get_steps(self):
        steps = {
            'x': self.splitter.get_cell_width(),
            'y': 0
        }
        return steps

    def draw_header(self):
        """Метод печатает заголовок таблциы"""
        header_list = self.get_header_list()
        point_x0, point_y0 = self.area.get_point()
        steps = self.get_steps()

        for column in header_list:
            if column == 'Команда':
                self.canvas.text(
                    xy=self.area.calculate_coord(point_x0=point_x0,
                                                 point_y0=point_y0,
                                                 size_x=self.splitter.get_row_name_width(),
                                                 size_y=self.area.get_text_size()[1],
                                                 text_size=self.canvas.\
                                                     textsize(column, self.get_font()),
                                                 anchor='lm'),
                    text=column,
                    font=self.get_font(),
                    fill=self.get_fill()
                )
                point_x0 += (self.splitter.get_row_name_width() +
                             self.area.__getattribute__('row_name_left_padding'))
            else:
                self.canvas.text(
                    xy=self.area.calculate_coord(point_x0=point_x0,
                                                 point_y0=point_y0,
                                                 size_x=steps['x'],
                                                 size_y=self.area.get_text_size()[1],
                                                 text_size=self.canvas.\
                                                     textsize(column, self.get_font()),
                                                 anchor=self.get_anchor()),
                    text=column,
                    font=self.get_font(),
                    fill=self.get_fill(),
                    align='center'
                )
                point_x0 += steps['x']


class TableData(Row):
    """Класс для работы с таблицей данных

    Args:
        Row (_type_): наследуемый класс для работы со строками таблицы данных
    """

    def set_settings(self,
                     padding=(0, 0, 0, 0),
                     row_name_left_padding=0,
                     font_path=None,
                     font_size=None,
                     fill=(255, 255, 255),
                     anchor='la'):
        super(TableData, self).set_settings(padding,
                                            row_name_left_padding,
                                            font_path,
                                            font_size,
                                            fill,
                                            anchor)
        self.set_row_name_width()

    def set_point(self, point_x0=None, point_y0=None):
        self.area.set_point(
            point_x0=self.area.get_padding()[1],
            point_y0=self.splitter.get_title_size()[1] + self.splitter.get_header_height()
        )

    def set_row_name_width(self):
        """Метод переберает самое длинное название команды и заносит его длину в разделитель"""
        max_width = 0
        for team in self.results_data:
            if self.canvas.textsize(team['Команда'], self.get_font())[0] > max_width:
                max_width = self.canvas.textsize(team['Команда'], self.get_font())[0]
        self.splitter.set_row_name_width(max_width)

    def get_steps(self):

        steps = {
            'x': self.splitter.get_cell_width(),
            'y': ((self.splitter.get_table_size()[1] -
                   self.area.get_padding()[0] -
                   self.splitter.get_header_height() -
                   self.area.get_padding()[1]) /
                  len(self.results_data))
        }
        return steps

    def draw_table(self):
        keys = self.get_keys()
        point_x0, point_y0 = self.area.get_point()
        steps = self.get_steps()

        for row in self.results_data:
            point_x0 = self.area.get_point()[0]
            for column in keys:
                if column == 'Команда':
                    self.canvas.text(
                        xy=self.area.calculate_coord(point_x0=point_x0,
                                                     point_y0=point_y0,
                                                     size_x=self.splitter.get_row_name_width(),
                                                     size_y=steps['y'],
                                                     text_size=self.canvas.\
                                                         textsize(str(row[column]),
                                                                  self.get_font()),
                                                     anchor='lm'),
                        text=str(row[column]),
                        font=self.get_font(),
                        fill=self.get_fill()
                    )
                    point_x0 += (self.splitter.get_row_name_width() +
                                 self.area.__getattribute__('row_name_left_padding'))
                else:
                    self.canvas.text(
                        xy=self.area.calculate_coord(point_x0=point_x0,
                                                     point_y0=point_y0,
                                                     size_x=steps['x'],
                                                     size_y=steps['y'],
                                                     text_size=self.canvas.\
                                                         textsize(
                                                             str(row[column]),
                                                             self.get_font()
                                                             ),
                                                     anchor=self.get_anchor()),
                        text=str(row[column]),
                        font=self.get_font(),
                        fill=self.get_fill(),
                        align='center'
                    )
                    point_x0 += steps['x']
            point_y0 += steps['y']


class TableSaver:
    """Сохранение таблиц"""

    def __init__(self, table: ResultsTable, path) -> None:
        self.img = table.img
        self.img.save(path)


class UpdateTables:
    """Класс для обновления таблиц"""

    def __init__(self) -> None:
        self.update_cup('Кубок туризма', 'data/img/results_new/tourism_result.jpg')
        self.update_cup('Кубок спорта', 'data/img/results_new/sport_result.jpg')
        self.update_cup('Кубок культуры', 'data/img/results_new/culture_result.jpg')
        self.update_cup('Кубок фестиваля', 'data/img/results_new/festival_result.jpg')
        self.update_cup('Кубок холдинга', 'data/img/results_new/holding_result.jpg')

    def update_cup(self, cup, file_path):
        """Обновление таблицы"""

        if cup == 'Кубок фестиваля':
            results_data = FestivalResult(holding=False).results
        elif cup == 'Кубок холдинга':
            results_data = HoldingResult(holding=True).results
        else:
            results_data = CupResults(cup).convert_to_display
        cup_results = ResultsTable(results_data)

        cup_results.title.draw_text(
            padding=(25, 25, 25, 25),
            text=cup,
            font_size=47,
            anchor='la'
        )

        cup_results.footer.draw_text(
            padding=(25, 25, 25, 25),
            text=f'* - последнее обновление таблицы: {datetime.now().strftime("%d.%m.%Y %H:%M")}',
            font_path='data/fonts/Montserrat-LightItalic.ttf',
            font_size=14,
            anchor='la'
        )

        cup_results.table.header.set_settings(
            padding=(0, 25, 25, 12.5),
            row_name_left_padding=25,
            font_path=None,
            font_size=18,
            anchor='mm'
        )

        cup_results.table.table_data.set_settings(
            padding=(0, 25, 25, 0),
            row_name_left_padding=25,
            font_path='data/fonts/Montserrat-Light.ttf',
            font_size=18,
            anchor='mm')

        cup_results.table.draw_table()
        TableSaver(cup_results, file_path)
