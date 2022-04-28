import discord
from discord.ext import commands
from settings import TOKEN, COMMAND_PREFIX
from text_game_bot import TextGameBot

if __name__ == '__main__':
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
    bot.add_cog(TextGameBot(bot))
    bot.run(TOKEN)
