from discord.ext import commands
from settings import COMMAND_PREFIX,DB
from bulls_and_cows import BullsAndCowsGame
from rock_paper_scissors import RockPaperScissorsGame
from settings import RPS_VARIANTS

class TextGameBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running_games = {}
        self.game_classes = {
            "1": BullsAndCowsGame,
            "2": RockPaperScissorsGame
        }


    def start_game(self,user,game_class):
        game = game_class()
        game.start()
        if user in self.running_games:
            return "Вы уже в игре"
        self.running_games[user] = game
        return f"Игра запущена\n{game_class.description}"


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if COMMAND_PREFIX == message.content[:len(COMMAND_PREFIX)]:
            return
        #await message.channel.send("Спасибо за сообщение")
        if message.author in self.running_games:
            game = self.running_games[message.author]
            res, is_game_finished = game.give_answer(message.content)
            if is_game_finished:
                self.running_games.pop(message.author)
            await message.channel.send(res)
        elif message.content.lower() in RPS_VARIANTS:
            game = RockPaperScissorsGame()
            game.start()
            res, is_game_finished = game.give_answer(message.content)
            await message.channel.send(res)

    @commands.command(name='play')
    async def play_games(self, ctx, game_number=""):

        if game_number == "":
            text = "1.Быки и коровы\n" \
                   "2.Камень, ножницы, бумага\n"
            text += "для запуска игры напишите !play номер_игры"
            await ctx.send(text)
        elif game_number in self.game_classes:
            game_class = self.game_classes[game_number]
            result = self.start_game(ctx.author,game_class)
            await ctx.send(result)
        else:
            await ctx.send("Игра не найдена")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        DB.add_user(member)
