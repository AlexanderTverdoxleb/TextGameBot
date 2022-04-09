from discord.ext import commands
import random

class BotCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='randint')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)