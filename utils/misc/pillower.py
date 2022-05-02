"""Пакет работы с таблицами результатов"""

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from utils.db_api.db_comands import get_event_name_by_cup


class TableResult:
    """Создание таблиц с результатами"""

    def __init__(
            self,
            background_img='data/img/results_new/background.jpg',
            title_font_way='data/fonts/Montserrat-Regular.ttf',
            title_font_size=47,
            table_header_font_way='data/fonts/Montserrat-Regular.ttf',
            table_header_font_size=23,
            table_data_font_way='data/fonts/Montserrat-Light.ttf',
            table_data_font_size=18,
            footer_font_way='data/fonts/Montserrat-LightItalic.ttf',
            footer_font_size=14,
            title_padding=(25, 25, 25, 25),
            table_padding=(0, 25, 25, 0),
            header_padding=(0, 0, 0, 10),
            first_column_padding=(0, 0, 25, 0),
            footer_padding=(25, 25, 25, 25),
            point_x0=0,
            point_x1=0,
            point_y0=0,
            point_y1=0,
            size_x=0,
            size_y=0,
            max_size_x=0,
            max_size_y=0
    ) -> None:

        self.table_background = Image.open(background_img)
        self.canvas = ImageDraw.Draw(self.table_background)

        self.title_font_way = title_font_way
        self.title_font_size = title_font_size
        self.title_font = ImageFont.truetype(
            font=self.title_font_way,
            size=self.title_font_size)

        self.table_header_font_way = table_header_font_way
        self.table_header_font_size = table_header_font_size
        self.table_header_font = ImageFont.truetype(
            font=self.table_header_font_way,
            size=self.table_header_font_size
        )

        self.table_data_font_way = table_data_font_way
        self.table_data_font_size = table_data_font_size
        self.table_data_font = ImageFont.truetype(
            font=self.table_data_font_way,
            size=self.table_data_font_size
        )

        self.footer_font_way = footer_font_way
        self.footer_font_size = footer_font_size
        self.footer_font = ImageFont.truetype(
            font=self.footer_font_way,
            size=self.footer_font_size
        )

        self.title_padding = title_padding
        self.table_padding = table_padding
        self.header_padding = header_padding
        self.first_column_padding = first_column_padding
        self.footer_padding = footer_padding

        self.point_x0, self.point_x1 = point_x0, point_x1
        self.point_y0, self.point_y1 = point_y0, point_y1
        self.size_x = size_x
        self.size_y = size_y
        self.max_size_x = max_size_x
        self.max_size_y = max_size_y
        self.point_y0 = 0
        self.point_y1 = self.table_background.size[1]

    def find_max_size(self, text_list: list, font: ImageFont):
        """Вычисляет максимальный размер из элементов списка

        Args:
            text_list (list): список текстов
            font (ImageFont): шрифт, применяемый для данного текста

        Returns:
            _type_: максимальная ширина и высота
        """
        for item in text_list:
            if self.max_size_x <= self.canvas.textsize(item, font)[0]:
                self.max_size_x = self.canvas.textsize(item, font)[0]
            if self.max_size_y <= self.canvas.textsize(item, font)[1]:
                self.max_size_y = self.canvas.textsize(item, font)[1]

    def calculate_point(
            self,
            area: tuple,
            text_size,
            anchor: str = 'la') -> tuple:
        """Вычисляет точку начала текста

        Args:
            area (tuple): область текста.(x0, y0, ширина области, высота области)
            text_size (_type_): размер текста
            anchor (str, optional): якорь. По умолчанию 'la'.

        Returns:
            tuple: координаты начала текста (x, y)
        """

        point_x = area[0]
        point_y = area[1]
        width = area[2]
        height = area[3]
        text_width = text_size[0]
        text_height = text_size[1]
        if anchor == 'la':
            return point_x, point_y
        elif anchor == 'ma':
            return point_x + width / 2 - text_width / 2, point_y
        elif anchor == 'ra':
            return width - text_width, point_y
        elif anchor == 'lm':
            return point_x, point_y + height / 2 - text_height / 2
        elif anchor == 'mm':
            return point_x + width / 2 - text_width / 2, point_y + height / 2 - text_height / 2
        elif anchor == 'rm':
            return width - text_width, point_y + height / 2 - text_height / 2
        elif anchor == 'lb':
            return point_x, height - text_height
        elif anchor == 'mb':
            return point_x + width / 2 - text_width / 2, height - text_height
        elif anchor == 'rb':
            return width - text_width, height - text_height
        else:
            print("Unknown position for text")
            return point_x, point_y

    def set_background(self, way: str):
        """устанавливает фон для картинки с результатами

        Args:
            way (str): месторасоположение фона
        """
        self.canvas = ImageDraw.Draw(Image.open(way))

    def set_title_font(self, way: str, size: int):
        """Устанавливает шрифт для заголовка

        Args:
            way (str): месторасоположение шрифта
            size (int): размер шрифта
        """
        self.title_font = ImageFont.truetype(font=way, size=size)

    def set_title_font_way(self, way: str):
        """Устанавливает шрифт для заголовка

        Args:
            way (str): месторасоположение шрифта
        """
        self.title_font_way = way
        self.title_font = ImageFont.truetype(
            font=self.title_font_way,
            size=self.title_font_size
        )

    def set_title_font_size(self, size: int):
        """Устанавливает размер шрифта для заголовка

        Args:
            size (int): размер шрифта
        """
        self.title_font_size = size
        self.title_font = ImageFont.truetype(
            font=self.title_font_way,
            size=self.title_font_size
        )

    def set_table_header_font(self, way: str, size: int):
        """Устанавливает шрифт для заголовка таблицы

        Args:
            way (str): месторасоположение шрифта
            size (int): размер шрифта
        """
        self.table_header_font = ImageFont.truetype(font=way, size=size)

    def set_table_header_font_way(self, way: str):
        """Устанавливает шрифт для заголовков таблицы

        Args:
            way (str): месторасоположение шрифта
        """
        self.table_header_font_way = way
        self.table_header_font = ImageFont.truetype(
            font=self.table_header_font_way,
            size=self.table_header_font_size
        )

    def set_table_header_font_size(self, size: int):
        """Устанавливает размер шрифта для заголовков таблицы

        Args:
            size (int): размер шрифта
        """
        self.table_header_font_size = size
        self.table_header_font = ImageFont.truetype(
            font=self.table_header_font_way,
            size=self.table_header_font_size
        )

    def set_table_data_font(self, way: str, size: int):
        """Устанавливает шрифт для данных таблицы

        Args:
            way (str): месторасоположение шрифта
            size (int): размер шрифта
        """
        self.table_data_font = ImageFont.truetype(font=way, size=size)

    def set_table_data_font_way(self, way: str):
        """Устанавливает шрифт для результатов таблицы

        Args:
            way (str): месторасоположение шрифта
        """
        self.table_data_font_way = way
        self.table_data_font = ImageFont.truetype(
            font=self.table_data_font_way,
            size=self.table_data_font_size
        )

    def set_table_data_font_size(self, size: int):
        """Устанавливает размер шрифта для результатов таблицы

        Args:
            size (int): размер шрифта
        """
        self.table_data_font_size = size
        self.table_data_font = ImageFont.truetype(
            font=self.table_data_font_way,
            size=self.table_data_font_size
        )

    def set_footer_font(self, way: str, size: int):
        """Устанавливает шрифт для футера

        Args:
            way (str): месторасоположение шрифта
            size (int): размер шрифта
        """
        self.footer_font = ImageFont.truetype(font=way, size=size)

    def set_footer_font_way(self, way: str):
        """Устанавливает шрифт для футура

        Args:
            way (str): месторасоположение шрифта
        """
        self.footer_font_way = way
        self.footer_font = ImageFont.truetype(
            font=self.footer_font_way,
            size=self.footer_font_size
        )

    def set_footer_font_size(self, size: int):
        """Устанавливает размер шрифта для футура

        Args:
            size (int): размер шрифта
        """
        self.footer_font_size = size
        self.footer_font = ImageFont.truetype(
            font=self.footer_font_way,
            size=self.footer_font_size
        )

    def set_title_padding(self, top: int, left: int, right: int, bottom: int):
        """Устанавливает отсутупы для загалова

        Args:
            top (int): отсутуп сверху
            left (int): отсутуп слева
            right (int): отсутуп справа
            bottom (int): отсутуп снизу
        """
        self.title_padding = (top, left, right, bottom)

    def set_table_padding(self, top: int, left: int, right: int, bottom: int):
        """Устанавливает отсутупы для таблицы

        Args:
            top (int): отсутуп сверху
            left (int): отсутуп слева
            right (int): отсутуп справа
            bottom (int): отсутуп снизу
        """
        self.table_padding = (top, left, right, bottom)

    def set_first_column_padding(self, top: int, left: int, right: int, bottom: int):
        """Устанавливает отсутупы для первой колонки таблицы

        Args:
            top (int): отсутуп сверху
            left (int): отсутуп слева
            right (int): отсутуп справа
            bottom (int): отсутуп снизу
        """
        self.first_column_padding = (top, left, right, bottom)

    def set_footer_padding(self, top: int, left: int, right: int, bottom: int):
        """Устанавливает отсутупы для футера

        Args:
            top (int): отсутуп сверху
            left (int): отсутуп слева
            right (int): отсутуп справа
            bottom (int): отсутуп снизу
        """
        self.footer_padding = (top, left, right, bottom)

    def set_title(self, title_text: str):
        """Устанавливает заголовок

        Args:
            title_text (str): текст заголовка
        """
        self.canvas.text(
            xy=(0 + self.title_padding[1], 0 + self.title_padding[0]),
            text=title_text,
            font=self.title_font
        )
        self.point_y0 = self.title_padding[0] \
            + self.canvas.textsize(title_text, self.title_font)[1] \
            + self.title_padding[3]

    def set_footer(self, footer_text: str):
        """Устанавливает футер

        Args:
            footer_text (str): тескт футера
        """
        self.canvas.text(
            xy=(
                self.footer_padding[1],
                self.table_background.size[1]
                - self.footer_padding[3]
                - self.canvas.textsize(footer_text, self.footer_font)[1]
            ),
            text=footer_text,
            font=self.footer_font
        )
        self.point_y1 = self.table_background.size[1]\
            - self.footer_padding[3]\
            - self.canvas.textsize(footer_text, self.footer_font)[1]\
            - self.footer_padding[0]

    def set_header(self, columns_list: list):
        """Устанавливает заголовки таблицы

        Args:
            columns_list (list): список заголовков
        """
        self.size_x = (self.table_background.size[0] -
                       self.header_padding[1] - self.header_padding[2] -
                       self.first_column_padding[2]) / len(columns_list)
        self.size_y = 0

        for column in columns_list:
            if self.size_y <= self.canvas.textsize(
                    text=column,
                    font=self.table_header_font)[1]:
                self.size_y = self.canvas.textsize(
                    text=column,
                    font=self.table_header_font)[1]

        self.point_x0 = self.table_padding[1]

        for column in columns_list:
            if column == "Команда":
                self.canvas.text(
                    xy=self.calculate_point(
                        area=(
                            self.point_x0, self.point_y0,
                            self.size_x, self.size_y
                        ),
                        text_size=self.canvas.textsize(
                            text=column,
                            font=self.table_header_font
                        ),
                        anchor='lm'
                    ),
                    text=column,
                    font=self.table_header_font,
                    align='left'
                )
                self.point_x0 += self.first_column_padding[2]
            else:
                self.canvas.text(
                    xy=self.calculate_point(
                        area=(
                            self.point_x0, self.point_y0,
                            self.size_x, self.size_y
                        ),
                        text_size=self.canvas.textsize(
                            text=column,
                            font=self.table_header_font
                        ),
                        anchor='mm'
                    ),
                    text=column,
                    font=self.table_header_font,
                    align='center'
                )
            self.point_x0 += self.size_x
        self.point_y0 += self.size_y + self.header_padding[3]

    def set_results(self, results_list: list):
        """Устанавливает таблицу с результатами

        Args:
            results_list (list): список списков результатов
        """
        self.size_y = (self.point_y1 - self.point_y0) / len(results_list)
        self.point_x0 = self.table_padding[1]
        self.point_x1 = self.table_background.size[0] - self.table_padding[2]
        for row in results_list:
            self.point_x0 = self.table_padding[1]
            for column in row:
                if self.point_x0 == self.first_column_padding[2]:
                    self.canvas.text(
                        xy=self.calculate_point(
                            area=(
                                self.point_x0, self.point_y0,
                                self.size_x, self.size_y
                            ),
                            text_size=self.canvas.textsize(
                                text=column,
                                font=self.table_data_font
                            ),
                            anchor='lm'
                        ),
                        text=column,
                        font=self.table_data_font
                    )
                    self.point_x0 += self.first_column_padding[2]
                else:
                    self.canvas.text(
                        xy=self.calculate_point(
                            area=(
                                self.point_x0, self.point_y0,
                                self.size_x, self.size_y
                            ),
                            text_size=self.canvas.textsize(
                                text=column,
                                font=self.table_data_font
                            ),
                            anchor='mm'
                        ),
                        text=column,
                        font=self.table_data_font
                    )
                self.point_x0 += self.size_x
            self.point_y0 += self.size_y

    def save_table(self, file_name: str):
        """Сохраняет изображением с таблицей результатов

        Args:
            file_name (str): имя файла с указанием пути
        """
        self.table_background.save(fp=file_name)

    def show_table(self):
        """ Открытие изображения"""
        self.table_background.show()


def set_result_of_tourism_table(event_type: str, results: list):
    """Обновление таблицы кубка туризма

    Args:
        event_type (str): тип кубка
        results (list): список результатов
    """

    # Создаем экземпляр класса TableResult для кубка туризма
    tourism_table = TableResult()

    # Устанавливаем заголовок
    tourism_table.set_title(event_type)

    # Устанавливаем футер
    tourism_table.set_footer(
        footer_text="Послендее обновление таблицы: "
                    + datetime.now().strftime('%d.%m %H:%M')
    )

    # Устанавливаем заголовки таблицы
    events_list = get_event_name_by_cup(event_type=event_type)
    columns_list = ['Команда']
    for event in events_list:
        columns_list.append(event.replace(' ', '\n'))
    columns_list.append('Кол-во\nочков')
    columns_list.append('Место')
    tourism_table.set_table_header_font_size(size=20)
    tourism_table.set_header(columns_list=columns_list)

    # Устанавливаем таблицу с результатами

    tourism_table.set_results(results_list=results)  # TODO: реализовать получение результатов

    # Сохраняем таблицу с результатами
    tourism_table.save_table(file_name='data/img/results_new/tourism_result.jpg')


def set_result_of_sport_table(event_type: str, results: list):
    """Обновление таблицы кубка туризма

    Args:
        event_type (str): тип кубка
        results (list): список результатов
    """

    # Создаем экземпляр класса TableResult для кубка туризма
    sport_table = TableResult()

    # Устанавливаем заголовок
    sport_table.set_title(event_type)

    # Устанавливаем футер
    sport_table.set_footer(
        footer_text="Послендее обновление таблицы: "
                    + datetime.now().strftime('%d.%m %H:%M')
    )

    # Устанавливаем заголовки таблицы
    events_list = get_event_name_by_cup(event_type=event_type)
    columns_list = ['Команда']
    for event in events_list:
        columns_list.append(event.replace(' ', '\n', 1))
    columns_list.append('Кол-во\nочков')
    columns_list.append('Место')
    sport_table.set_table_header_font_size(size=18)
    sport_table.set_header(columns_list=columns_list)

    # Устанавливаем таблицу с результатами

    sport_table.set_results(results_list=results)  # TODO: реализовать получение результатов

    # Сохраняем таблицу с результатами
    sport_table.save_table(file_name='data/img/results_new/sport_result.jpg')


def set_result_of_culture_table(event_type: str, results: list):
    """Обновление таблицы кубка туризма

    Args:
        event_type (str): тип кубка
        results (list): список результатов
    """

    # Создаем экземпляр класса TableResult для кубка туризма
    culture_table = TableResult()

    # Устанавливаем заголовок
    culture_table.set_title(event_type)

    # Устанавливаем футер
    culture_table.set_footer(
        footer_text="Послендее обновление таблицы: "
                    + datetime.now().strftime('%d.%m %H:%M')
    )

    # Устанавливаем заголовки таблицы
    events_list = get_event_name_by_cup(event_type=event_type)
    columns_list = ['Команда']
    for event in events_list:
        columns_list.append(event.replace(' ', '\n', 1))
    columns_list.append('Кол-во\nочков')
    columns_list.append('Место')
    culture_table.set_header(columns_list=columns_list)

    # Устанавливаем таблицу с результатами

    culture_table.set_results(results_list=results)  # TODO: реализовать получение результатов

    # Сохраняем таблицу с результатами
    culture_table.save_table(file_name='data/img/results_new/culture_result.jpg')


def set_result_festival_table(event_type: str, results: list):
    """Обновление кубка фестиваля

    Args:
        event_type (str): _description_
        results (list): таблица результатов
    """

    # Создаем экземпляр класса TableResult для кубка туризма
    festival_table = TableResult()

    # Устанавливаем заголовок
    festival_table.set_title(event_type)

    # Устанавливаем футер
    festival_table.set_footer(
        footer_text="Послендее обновление таблицы: "
                    + datetime.now().strftime('%d.%m %H:%M')
    )

    # Устанавливаем заголовки таблицы
    columns_list = [
        'Команда',
        'Кубок\nтуризма',
        'Кубок\nспорта',
        'Кубок\nкультуры',
        'Кол-во\nочков',
        'Место'
    ]
    festival_table.set_header(columns_list=columns_list)

    # Устанавливаем таблицу с результатами

    festival_table.set_results(results_list=results)  # TODO: реализовать получение результатов

    # Сохраняем таблицу с результатами
    festival_table.save_table(file_name='data/img/results_new/festival_result.jpg')


def set_result_holding_table(event_type: str, results: list):
    """Обновление кубка холдинга

    Args:
        event_type (str): _description_
        results (list): таблица результатов
    """

    # Создаем экземпляр класса TableResult для кубка туризма
    holding_table = TableResult()

    # Устанавливаем заголовок
    holding_table.set_title(event_type)

    # Устанавливаем футер
    holding_table.set_footer(
        footer_text="Послендее обновление таблицы: "
                    + datetime.now().strftime('%d.%m %H:%M')
    )

    # Устанавливаем заголовки таблицы
    columns_list = [
        'Команда',
        'Кубок\nтуризма',
        'Кубок\nспорта',
        'Кубок\nкультуры',
        'Кол-во\nочков',
        'Место'
    ]
    holding_table.set_header(columns_list=columns_list)

    # Устанавливаем таблицу с результатами

    holding_table.set_results(results_list=results)  # TODO: реализовать получение результатов

    # Сохраняем таблицу с результатами
    holding_table.save_table(file_name='data/img/results_new/holding_result.jpg')


def update_result_table(event_type: str):
    """обновление таблиц результатов

    Args:
        event_type (str): название кубка, результат которого был обновлен
    TODO: Рассмотреть реализацию timezone из библиотеки pytz
    """
    # Обновление кубка
    if event_type == 'Кубок туризма':

        results_list_tourism = [
            ["Прокат", "1/50", "1/50", "1/50", "1/50", "1/50", "150", "1"],
            ["ГКС+Меттранс", "2/51", "2/51", "2/51", "2/51", "2/51", "153", "2"],
            ["Сталь", "3/54", "3/54", "3/54", "3/54", "3/54", "162", "3"],
            ["РАЗАМ", "3/54", "3/54", "3/54", "3/54", "3/54", "162", "3"],
            ["Белвторчермет", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "5"],
            ["МПЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "6"],
            ["ЗУбры", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "7"],
            ["РМЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "8"],
            ["ByCord", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "9"],
            ["Интеграл", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "10"],
            ["МЗКТ", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "11"],
            ["МАЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "12"],
            ["Могилевлифтмаш", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "13"],
            ["ММЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "14"]
        ]

        set_result_of_tourism_table(
            event_type=event_type,
            results=results_list_tourism
        )
    elif event_type == 'Кубок спорта':
        results_list_sport = [
            ["Прокат", "1/50", "1/50", "1/50", "1/50", "1/50", "1/50", "150", "1"],
            ["ГКС+Меттранс", "2/51", "2/51", "2/51", "2/51", "2/51", "1/50", "153", "2"],
            ["Сталь", "3/54", "3/54", "3/54", "3/54", "3/54", "1/50", "162", "3"],
            ["РАЗАМ", "3/54", "3/54", "3/54", "3/54", "3/54", "1/50", "162", "3"],
            ["Белвторчермет", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "5"],
            ["МПЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "6"],
            ["ЗУбры", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "7"],
            ["РМЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "8"],
            ["ByCord", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "9"],
            ["Интеграл", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "10"],
            ["МЗКТ", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "11"],
            ["МАЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "12"],
            ["Могилевлифтмаш", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "13"],
            ["ММЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "-//-", "14"]
        ]
        set_result_of_sport_table(
            event_type=event_type,
            results=results_list_sport
        )
    elif event_type == 'Кубок культуры':
        results_list_culture = [
            ["Прокат", "1/50", "1/50", "1/50", "1/50", "150", "1"],
            ["ГКС+Меттранс", "2/51", "2/51", "2/51", "1/50", "153", "2"],
            ["Сталь", "3/54", "3/54", "3/54", "3/54", "162", "3"],
            ["РАЗАМ", "3/54", "3/54", "3/54", "3/54", "162", "3"],
            ["Белвторчермет", "-//-", "-//-", "-//-", "-//-", "-//-", "5"],
            ["МПЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "6"],
            ["ЗУбры", "-//-", "-//-", "-//-", "-//-", "-//-", "7"],
            ["РМЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "8"],
            ["ByCord", "-//-", "-//-", "-//-", "-//-", "-//-", "9"],
            ["Интеграл", "-//-", "-//-", "-//-", "-//-", "-//-", "10"],
            ["МЗКТ", "-//-", "-//-", "-//-", "-//-", "-//-", "11"],
            ["МАЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "12"],
            ["Могилевлифтмаш", "-//-", "-//-", "-//-", "-//-", "-//-", "13"],
            ["ММЗ", "-//-", "-//-", "-//-", "-//-", "-//-", "14"]
        ]
        set_result_of_culture_table(
            event_type=event_type,
            results=results_list_culture
        )
    else:
        print("Неожиданный результат переданный в update_result_table")

    # Обновление кубка фестиваля
    results_list_festival = [
        ["Прокат", "1/50", "1/50", "1/50", "150", "1"],
        ["ГКС+Меттранс", "2/51", "2/51", "2/51", "153", "2"],
        ["Сталь", "3/54", "3/54", "3/54", "162", "3"],
        ["РАЗАМ", "3/54", "3/54", "3/54", "162", "3"],
        ["Белвторчермет", "-//-", "-//-", "-//-", "-//-", "5"],
        ["МПЗ", "-//-", "-//-", "-//-", "-//-", "6"],
        ["ЗУбры", "-//-", "-//-", "-//-", "-//-", "7"],
        ["РМЗ", "-//-", "-//-", "-//-", "-//-", "8"],
        ["ByCord", "-//-", "-//-", "-//-", "-//-", "9"],
        ["Интеграл", "-//-", "-//-", "-//-", "-//-", "10"],
        ["МЗКТ", "-//-", "-//-", "-//-", "-//-", "11"],
        ["МАЗ", "-//-", "-//-", "-//-", "-//-", "12"],
        ["Могилевлифтмаш", "-//-", "-//-", "-//-", "-//-", "13"],
        ["ММЗ", "-//-", "-//-", "-//-", "-//-", "14"]
    ]
    set_result_festival_table(event_type="Кубок фестиваля", results=results_list_festival)

    # Обновление кубка холдинга
    results_list_holding = [
        ["Прокат", "1/50", "1/50", "1/50", "150", "1"],
        ["ГКС+Меттранс", "2/51", "2/51", "2/51", "153", "2"],
        ["Сталь", "3/54", "3/54", "3/54", "162", "3"],
        ["РАЗАМ", "3/54", "3/54", "3/54", "162", "3"],
        ["Белвторчермет", "-//-", "-//-", "-//-", "-//-", "5"],
        ["МПЗ", "-//-", "-//-", "-//-", "-//-", "6"],
        ["ЗУбры", "-//-", "-//-", "-//-", "-//-", "7"],
        ["РМЗ", "-//-", "-//-", "-//-", "-//-", "8"],
        ["ByCord", "-//-", "-//-", "-//-", "-//-", "9"],
        ["Интеграл", "-//-", "-//-", "-//-", "-//-", "10"],
        ["МЗКТ", "-//-", "-//-", "-//-", "-//-", "11"],
        ["МАЗ", "-//-", "-//-", "-//-", "-//-", "12"],
        ["Могилевлифтмаш", "-//-", "-//-", "-//-", "-//-", "13"],
        ["ММЗ", "-//-", "-//-", "-//-", "-//-", "14"]
    ]
    set_result_holding_table(event_type="Кубок фестиваля", results=results_list_holding)
