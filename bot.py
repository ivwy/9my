import discord
from discord.ext import commands

import json
import os

from colorama import Back, Fore, Style
import time
import platform

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Token": "", "Prefix": "!"}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]
bot = commands.Bot(command_prefix = prefix, intents = discord.Intents.all())

@bot.event
async def on_ready():
    prfx = (Back.BLACK + Fore.RED + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prfx + " Logged in as " + Fore.RED + bot.user.name)
    print(prfx + " Bot ID " + Fore.RED + str(bot.user.id))
    print(prfx + " Discord Version " + Fore.RED + discord.__version__)
    print(prfx + " Python Version " + Fore.RED + str(platform.python_version()))
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "Type !help for commands"))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token)