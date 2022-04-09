import random
class BullsAndCowsGame:
    def __init__(self):
        self.number = None
        self.attempt = 6
        self.len_number = 4
        self.move = 0

    def start(self):
        numbers = ("0","1","2","3","4","5","6","7","8","9")
        self.number = random.sample(numbers, self.len_number)

    def give_answer(self,answer):
        if self.number is None:
            return "Игра не инициализирована"
        self.move += 1
        if self.move >= self.attempt:
            right_answer = "".join(self.number)
            return f"Игра окончена. Загаданное число {right_answer}"
        if len(answer) != self.len_number:
            return "Введите 4-х значное число"
        cows = 0
        bulls = 0
        for i, elem in enumerate(self.number):
            if answer[i] == elem:
                bulls += 1
            elif answer[i] in self.number:
                cows += 1
        if bulls == self.len_number:
            return "Вы выиграли"
        return f"Количество коров: {cows}; Количество быков: {bulls}"
if __name__ == '__main__':
    game = BullsAndCowsGame()
    game.start()
    for i in range(10):
        answer = input()
        print(game.give_answer(answer))