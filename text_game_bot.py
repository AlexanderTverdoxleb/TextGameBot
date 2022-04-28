import discord
from discord.ext import commands
from settings import COMMAND_PREFIX, DB
from bulls_and_cows import BullsAndCowsGame
from rock_paper_scissors import RockPaperScissorsGame
from settings import RPS_VARIANTS, IMG_DIRECTORY
from spotify_api import SpotifyApi


class TextGameBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running_games = {}
        self.game_classes = {
            "1": BullsAndCowsGame,
            "2": RockPaperScissorsGame
        }

    def start_game(self, user, game_class):
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
        if message.author in self.running_games:
            game = self.running_games[message.author]
            res, is_game_finished = game.give_answer(message.content, message.author)
            if is_game_finished:
                self.running_games.pop(message.author)
            await message.channel.send(res)
        elif message.content.lower() in RPS_VARIANTS:
            game = RockPaperScissorsGame()
            game.start()
            res, is_game_finished = game.give_answer(message.content, message.author)
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
            result = self.start_game(ctx.author, game_class)
            await ctx.send(result)
        else:
            await ctx.send("Игра не найдена")

    @commands.command(name='stat')
    async def statistics(self, ctx):
        stat = DB.get_stat(ctx.author)
        stat_str = "Побед/поражений/ничей" + "\n" + "\n".join(f"{k} - {v}" for k, v in stat.items())
        await ctx.send(stat_str)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        DB.add_user(member)

    @commands.command(name='music')
    async def search_track(self, ctx, track_name=""):
        if track_name == "":
            await ctx.send("Для поиска трека надо ввести комануд(!music "'исполнитель'"-"'название_трека'")")
        else:
            api_object = SpotifyApi()
            try:
                img_name, track_url = api_object.search(track_name)
                img_file = discord.File(f"{IMG_DIRECTORY}/{img_name}")
                await ctx.send(track_url, file=img_file)
            except ValueError as error:
                await ctx.send(str(error))
