import sqlite3


class GameStat:
    def __init__(self, count_wins=0, count_loses=0, count_draws=0):
        self.count_wins = count_wins
        self.count_loses = count_loses
        self.count_draws = count_draws

    def __str__(self):
        return f"{self.count_wins}/{self.count_loses}/{self.count_draws}"


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite3")

    def add_user(self, user):
        cursor = self.connection.cursor()
        res = cursor.execute(f"""insert into users (discriminator) values ('{user.discriminator}')""").fetchall()
        self.connection.commit()

    def add_game(self, game_name):
        cursor = self.connection.cursor()
        res = cursor.execute(f"""insert into games (game_name) values ('{game_name}')""").fetchall()
        self.connection.commit()

    def add_result(self, result, game_name, user):
        user_id = self._get_id("users", user.discriminator, "discriminator")
        game_id = self._get_id("games", game_name, "game_name")
        if result:
            status = "true"
        elif result is None:
            status = "null"
        else:
            status = "false"
        cursor = self.connection.cursor()
        res = cursor.execute(f"insert into user_results (user_id,game_id,status) "
                             f"values ({user_id},{game_id},{status})").fetchall()
        self.connection.commit()

    def _get_id(self, table_name, value, column_name):
        cursor = self.connection.cursor()
        res = cursor.execute(f"""SELECT id FROM {table_name} WHERE {column_name} = '{value}'""").fetchall()
        if len(res) == 0:
            raise ValueError("Пустой результат")
        return res[0][0]

    def get_stat(self, user):
        user_id = self._get_id("users", user.discriminator, "discriminator")
        cursor = self.connection.cursor()
        res = cursor.execute(f"SELECT game_name,status FROM user_results INNER JOIN"
                             f" games ON user_results.game_id = games.id WHERE user_id = {user_id}")
        stat = {}
        for row in res:
            if row[0] not in stat:
                stat[row[0]] = GameStat()
            if row[1] is None:
                stat[row[0]].count_draws += 1
            elif row[1]:
                stat[row[0]].count_wins += 1
            else:
                stat[row[0]].count_loses += 1
        return stat
