import random
from settings import RPS_VARIANTS


class RockPaperScissorsGame:
    description = "ghfdbkf"
    def __init__(self):
        self.chosen_variant = ""

    def start(self):
        self.chosen_variant = random.sample(RPS_VARIANTS, 1)[0]

    def give_answer(self, answer):
        if self.chosen_variant == "":
            return "Игра не инициализирована", True
        answer = answer.lower()
        if answer not in RPS_VARIANTS:
            return "Нет такого варианта", False
        if answer == self.chosen_variant:
            return f"{self.chosen_variant}\nничья", True


        if answer == "камень":
            if self.chosen_variant == "ножницы":
                return "ножницы \nвы победили", True
            return "бумага \nвы проиграли", True


        if answer == "ножницы":
            if self.chosen_variant == "бумага":
                return "бумага \nвы победили", True
            return "камень \nвы проиграли", True


        if answer == "бумага":
            if self.chosen_variant == "камень":
                return "камень \nвы победили", True
            return "ножницы \nвы проиграли", True