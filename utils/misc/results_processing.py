"""Пакет для обработки результатов"""

from operator import itemgetter

from utils.db_api.db_comands import get_event_coefficient, get_event_name,\
    get_events_list, get_place, get_team_name, get_teams_list


class Result:
    """Класс для обработки одного результата"""

    def __init__(self, team_id, event_id) -> None:
        self.team_id = team_id
        self.event_id = event_id
        self.coefficient = get_event_coefficient(self.event_id)
        self.place = get_place(self.team_id, self.event_id)

    @property
    def team_id(self):
        """team_id"""
        return self.__team_id

    @team_id.setter
    def team_id(self, team_id):
        self.__team_id = team_id

    @property
    def team_name(self):
        """Метод получени team_name из БД

        Returns:
            _type_: _description_
        """
        return get_team_name(self.team_id)

    @property
    def event_name(self):
        """Метод получения event_name из БД

        Returns:
            _type_: _description_
        """
        return get_event_name(self.event_id)

    @property
    def event_id(self):
        """event_id"""
        return self.__event_id

    @event_id.setter
    def event_id(self, event_id):
        self.__event_id = event_id

    @property
    def coefficient(self):
        """coefficient"""
        return self.__coefficient

    @coefficient.setter
    def coefficient(self, coefficient):
        self.__coefficient = coefficient

    @property
    def point(self):
        """Метод возвращает количество очков за данный конкурс

        Returns:
            float: кол-во очков
        """
        if isinstance(self.place, int):
            return self.place * self.coefficient
        else:
            return '-'

    @property
    def text_result(self) -> str:
        """МЕтод отображения результатов

        Raises:
            TypeError: _description_

        Returns:
            str: результат в формате 'место/ кол-во очков'
        """
        return f"{self.place}/{self.point}"


class FestivalResult:
    """Класс для работы с резульаттами кубка фестиваля"""

    def __init__(self, holding=False) -> None:
        self.holding = holding
        self.results = None
        self.sum_point()
        self.distribute_places_with_pass()

    @property
    def holding(self):
        """get holding"""
        return self.__holding

    @holding.setter
    def holding(self, holding):
        if not isinstance(holding, bool):
            raise TypeError('Значение holding должно быть True или False')
        self.__holding = holding

    @property
    def results(self):
        """get results"""
        return self.__results

    @results.setter
    def results(self, results):
        self.__results = []
        if results is None:

            tourism_cup = CupResults('Кубок туризма', self.holding).convert_to_short_display
            sport_cup = CupResults('Кубок спорта', self.holding).convert_to_short_display
            culture_cup = CupResults('Кубок культуры', self.holding).convert_to_short_display

            self.__results = self.join_results(
                self.join_results(tourism_cup,sport_cup),
                culture_cup
            )

        else:
            self.__results = results

    @staticmethod
    def join_results(li1, li2) -> list:
        """Метод объединения двух списков в один

        Args:
            li1 (_type_): списко словарей
            li2 (_type_): список словарей

        Returns:
            list: список словарей в формате:
                {
                    'Команда': team_name,
                    'Кубок 1': point,
                    'Кубок 2': point,
                    'Кол-во очков': point,
                    'Место': place
                }
        """
        for elem1 in li1:
            team_name = elem1['Команда']
            for elem2 in li2:
                if elem2['Команда'] == team_name:
                    elem1.update(elem2)
        return li1

    def sum_point(self):
        """Метод подсчета количества очков"""

        for result in self.__results:
            summ = 0
            columns = result.keys()
            for column in columns:
                if column != 'Команда':
                    if result[column] != '-/-':
                        summ += float(result[column].split('/')[1])
            result.update({'Кол-во очков': summ})

    def sort_results(self, sortable_column='Кол-во очков'):
        """Метод сортировки списка результатов по количеству очков"""
        self.results.sort(key=itemgetter(sortable_column))

    def distribute_places_with_pass(self):
        """Метод распределяет места с пропуском мест при повторении
        и добавляет колонку в результаты"""
        self.sort_results()

        counter = 0
        place = 0
        previous_result = 0
        for result in self.__results:
            if result['Кол-во очков'] != previous_result:
                if counter == 0:
                    previous_result = result['Кол-во очков']
                    place += 1
                    result.update({'Место': place})
                else:
                    previous_result = result['Кол-во очков']
                    place += 1 + counter
                    result.update({'Место': place})
                    counter = 0
            else:
                result.update({'Место': place})
                counter += 1

    def distribute_places_withot_pass(self):
        """Метод распределяет места без пропуска мест при повторении
        и добавляет колонку в результаты"""

        self.sort_results()

        place = 0
        previous_result = 0
        for result in self.__results:

            if result['Кол-во очков'] != previous_result:
                previous_result = result['Кол-во очков']
                place += 1
                result.update({'Место': place})
            else:
                result.update({'Место': place})


class CupResults:
    """Класс для работы с результатами"""

    def __init__(self, cup, holding=False):
        self.cup = cup
        self.teams = get_teams_list(holding)
        self.events = get_events_list(self.cup)
        self.results = None
        self.sum_point()
        self.distribute_places_with_pass()

    @property
    def cup(self):
        """cup"""
        return self.__cup

    @cup.setter
    def cup(self, cup):
        if not isinstance(cup, str):
            raise TypeError('Значение кубка должно быть формата str')
        self.__cup = cup

    @property
    def teams(self):
        """Гетер списка команд"""
        return self.__teams

    @teams.setter
    def teams(self, teams):
        self.__teams = []
        for team in teams:
            self.__teams.append(team['item_id'])

    @property
    def events(self):
        """гетер конкурсов"""
        return self.__events

    @events.setter
    def events(self, events):
        self.__events = []
        for event in events:
            self.__events.append(event['item_id'])

    @property
    def results(self):
        """Гетер списка результатов"""
        return self.__results

    @results.setter
    def results(self, results):
        if results is None:
            self.__results = self.cup_results
        else:
            self.__results = results

    @property
    def cup_results(self):
        """Метод добавления получения списка результатов кубка

        Returns:
            list: список словарей в формате:
                'Команда': team_name,
                'event_name_1': class__Result,
                'event_name_2': class__Result,
                ...
                'event_name_n': class__Result

        """
        cup_results = []
        for team in self.teams:
            team_results = {
                'Команда': get_team_name(team)
            }
            for event in self.events:
                team_results.update(
                    {
                        get_event_name(event): Result(team, event)
                    }
                )
            cup_results.append(team_results)
        return cup_results

    def sum_point(self):
        """Метод подсчета количества очков"""

        for result in self.__results:
            summ = 0
            columns = result.keys()
            for column in columns:
                if column != 'Команда':
                    if result[column].point != '-':
                        summ += result[column].point
            result.update({'Кол-во очков': summ})

    def sort_results(self, sortable_column='Кол-во очков'):
        """Метод сортировки списка результатов по количеству очков"""

        self.results.sort(key=itemgetter(sortable_column))

    def distribute_places_with_pass(self):
        """Метод распределяет места с пропуском мест при повторении
        и добавляет колонку в результаты"""
        self.sort_results()

        counter = 0
        place = 0
        previous_result = 0
        for result in self.__results:
            if result['Кол-во очков'] != previous_result:
                if counter == 0:
                    previous_result = result['Кол-во очков']
                    place += 1
                    result.update({'Место': place})
                else:
                    previous_result = result['Кол-во очков']
                    place += 1 + counter
                    result.update({'Место': place})
                    counter = 0
            else:
                result.update({'Место': place})
                counter += 1

    def distribute_places_withot_pass(self):
        """Метод распределяет места без пропуска мест при повторении
        и добавляет колонку в результаты"""

        self.sort_results()

        place = 0
        previous_result = 0
        for result in self.__results:

            if result['Кол-во очков'] != previous_result:
                previous_result = result['Кол-во очков']
                place += 1
                result.update({'Место': place})
            else:
                result.update({'Место': place})

    # Метод для отображени результатов
    @property
    def convert_to_display(self) -> list:
        """Мето для отображения в результатах кубка

        Returns:
            list: список словарей в формате
                {
                    'Команда': team_name,
                    'Название конкурса 1': place/point,
                    'Названеи конкурса 2': place/point,
                    ...
                    'Название конкурса 3': place/point,
                    'Кол-во очко': summ_point,
                    'Место': place
                }
        """
        text_results = []

        for result in self.__results:
            result_dict = {}
            columns = result.keys()

            for column in columns:

                if column not in ['Команда', 'Кол-во очков', 'Место']:
                    if result[column] != '-':
                        result_dict.update({column: result[column].text_result})
                    else:
                        result_dict.update({column: '-'})
                else:
                    result_dict.update({column: result[column]})

            text_results.append(result_dict)

        return text_results

    # Метод для отображени ярезультатов в кубке фестиваля
    @property
    def convert_to_short_display(self) -> list:
        """Метод для отображени ярезультатов в кубке фестиваля и в кубкке холдинга

        Returns:
            list: список словарей в формате
                {
                    'Команда': team_name,
                    'Название кубка': place/point
                }
        """
        text_results = []

        for result in self.__results:
            text_results.append(
                {
                    'Команда': result['Команда'],
                    self.cup: f"{result['Место']}/{result['Кол-во очков']}"
                }
            )

        return text_results

def show_test_data():
    """тестовая функция
    """
    test_data = FestivalResult()
    # test_data = CupResults('Кубок спорта')


    print(test_data.results)
