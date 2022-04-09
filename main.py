from text_game_bot import TextGameBotClient
from settings import TOKEN
from discord.ext import commands
import discord
from bot_commands import BotCommands

if __name__ == '__main__':
    # client = TextGameBotClient()
    # client.run(TOKEN)
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.add_cog(BotCommands(bot))
    bot.run(TOKEN)