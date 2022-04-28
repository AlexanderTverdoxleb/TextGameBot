from settings import DB
import random


class BullsAndCowsGame:
    description = "Игрок, начинает игру, делает первую попытку отгадать число." + "\n" + \
                  "Попытка — это 4-значное число с неповторяющимися цифрами, сообщаемое боту." + "\n" + \
                  "Бот сообщает в ответ, сколько цифр угадано без совпадения с их позициями в тайном числе" + "\n" + \
                  "(то есть количество коров) и сколько угадано вплоть до позиции" \
                  " в тайном числе (то есть количество быков)." + "\n" + \
                  "Например: Задумано тайное число 3219 " + "\n" + \
                  "Попытка: 2310 Результат: две коровы (две цифры: 2 и 3 — угаданы на неверных позициях)" \
                  "и один бык (одна цифра 1 угадана вплоть до позиции)."
    game_name = 'Быки и коровы'

    def __init__(self):
        self.number = None
        self.attempt = 10
        self.len_number = 4
        self.move = 0

    def start(self):
        numbers = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        self.number = random.sample(numbers, self.len_number)

    def give_answer(self, answer, user):
        if self.number is None:
            return "Игра не инициализирована", True
        if len(answer) != self.len_number:
            return "Введите 4-х значное число", False
        if "".join(self.number) == answer:
            DB.add_result(True, self.game_name, user)
            return "Вы выиграли", True
        self.move += 1
        if self.move >= self.attempt:
            right_answer = "".join(self.number)
            DB.add_result(False, self.game_name, user)
            return f"Игра окончена. Загаданное число {right_answer}", True
        cows = 0
        bulls = 0
        for i, elem in enumerate(self.number):
            if answer[i] == elem:
                bulls += 1
            elif answer[i] in self.number:
                cows += 1
        return f"Количество коров: {cows}; Количество быков: {bulls}", False
