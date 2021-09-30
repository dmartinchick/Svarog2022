from datetime import datetime
from data import config
from mysql.connector import connect, Error
from utils.misc.other import convert_to_list


class SQLighter:

    def __init__(self) -> None:
        try:
            self.myconn=connect(
                host = config.HOST,
                user = config.USER,
                password = config.PASSWORD,
                database = config.DB,
            )
            self.cur = self.myconn.cursor()
            print('connect to DB')
        except Error as e:
            print(e)


    def reconnect(self):
        self.myconn.close()
        self.__init__()

    # Методы извлечения данных
    def get_date_start(self):
        self.reconnect()
        self.cur.execute("SELECT MIN(time_start) FROM `schedule`;")
        self.result = self.cur.fetchone()
        return self.result[0]

    
    def get_date_end(self):
        self.reconnect()
        self.cur.execute("SELECT MAX(time_end) FROM schedule;")
        self.result = self.cur.fetchone()
        return self.result[0]


    def what_now_db(self, tdate):
        """Возвращает пользователю список кортежей с мероприятиями

        Args:
            tdate (datetime): текущее время и дата

        Returns:
            list: список кортежей с мероприятиями
        """
        self.reconnect()

        self.cur.execute("SELECT name, time_start, time_end "
                        "FROM schedule INNER JOIN event ON schedule.event_name_id = event.id "
                        "WHERE time_start <= '%s' AND time_end >= '%s'" % (tdate, tdate))
        self.result = self.cur.fetchall()
        return self.result


    def what_next_db(self, tdate):
        self.reconnect()

        self.cur.execute("SELECT `name`, `time_start` "
                        "FROM `schedule` INNER JOIN `event` " 
                        "ON `schedule`.`event_name_id` = `event`.`id` "
                        "WHERE `time_start` > '%s' " 
                        "ORDER BY `time_start` "
                        "LIMIT 2;"%(tdate))
        self.result = self.cur.fetchall()
        return self.result
    

    def contests_db(self, name_en):
        self.reconnect()

        self.cur.execute("SELECT `name`, `type`, `coefficient`, `rule`, `composition`, `time_start` " 
                        "FROM `schedule` INNER JOIN `event` "
                        "ON `schedule`.`event_name_id` = `event`.`id` "
                        "WHERE `event`.`name_en` = '%s';"%(name_en))
        self.result = self.cur.fetchone()
        return self.result


    def get_users(self):
        self.reconnect()

        self.cur.execute("SELECT user_id FROM users;")
        self.result = self.cur.fetchall()
        return self.result

    def get_teams_all(self):
        self.reconnect()

        self.cur.execute("SELECT name, id FROM team;")
        self.result = self.cur.fetchall()
        return convert_to_list(self.result)

    def get_events_all(self):
        self.reconnect()

        self.cur.execute("SELECT name, id FROM event;")
        self.result = self.cur.fetchall()
        return convert_to_list(self.result)

    def get_team_subs(self, user_id):
        self.reconnect()

        self.cur.execute("SELECT team.name, team.id FROM subscriptions "
                        "JOIN team "
                        "ON team.id=subscriptions.team_id "
                        "WHERE subscriptions.user_id=%s;"%user_id)
        self.result = self.cur.fetchall()
        return convert_to_list(self.result)

    def get_event_subs(self, user_id):
        self.reconnect()

        self.cur.execute("SELECT event.name, event.id FROM subscriptions "
                        "JOIN event "
                        "ON event.id=subscriptions.event_id "
                        "WHERE subscriptions.user_id=%s;"%user_id)
        self.result = self.cur.fetchall()
        return convert_to_list(self.result)


    # Методы добавления данных
    def set_user(self,user_id):
        self.reconnect()

        self.cur.execute("INSERT INTO users (user_id, team_subs, event_subs) "
                        "VALUES (%s,NULL, NULL);"%(user_id))
        self.myconn.commit()


SQL = SQLighter()
