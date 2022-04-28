import random
from settings import RPS_VARIANTS, DB


class RockPaperScissorsGame:
    description = "Одновременно выбирают один из трех вариантов: камень, ножницы или бумагу." + "\n" + \
                  "Победитель определяется по следующим правилам:" + "\n" + \
                  "Бумага побеждает камень (бумага обёртывает камень)." + "\n" + \
                  "Камень побеждает ножницы (камень затупляет или ломает ножницы)." + "\n" + \
                  "Ножницы побеждают бумагу (ножницы разрезают бумагу)." + "\n" + \
                  "Если игроки выбрали одинаковый знак, то засчитывается ничья."
    game_name = 'Камень ножницы бумага'

    def __init__(self):
        self.chosen_variant = ""

    def start(self):
        self.chosen_variant = random.sample(RPS_VARIANTS, 1)[0]

    def give_answer(self, answer, user):
        if self.chosen_variant == "":
            return "Игра не инициализирована", True
        answer = answer.lower()
        if answer not in RPS_VARIANTS:
            return "Нет такого варианта", False
        if answer == self.chosen_variant:
            DB.add_result(None, self.game_name, user)
            return f"{self.chosen_variant}\nничья", True

        if answer == "камень":
            if self.chosen_variant == "ножницы":
                DB.add_result(True, self.game_name, user)
                return "ножницы \nвы победили", True
            DB.add_result(False, self.game_name, user)
            return "бумага \nвы проиграли", True

        if answer == "ножницы":
            if self.chosen_variant == "бумага":
                DB.add_result(True, self.game_name, user)
                return "бумага \nвы победили", True
            DB.add_result(False, self.game_name, user)
            return "камень \nвы проиграли", True

        if answer == "бумага":
            if self.chosen_variant == "камень":
                DB.add_result(True, self.game_name, user)
                return "камень \nвы победили", True
            DB.add_result(False, self.game_name, user)
            return "ножницы \nвы проиграли", True
