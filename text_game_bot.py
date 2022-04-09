import discord
from discord.ext import commands
import random

class TextGameBotClient(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return
        await message.channel.send("Спасибо за сообщение")

    @commands.command(name='randint')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)