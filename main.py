import os
import discord
from discord.ext import commands
import config 
from defines import printex, ConnectToDatabase
from prettytable import PrettyTable
intents = discord.Intents.all()
bot = commands.Bot(command_prefix= "nlrp!", intents= intents)

PrettyTable.vertical_char = "│"
PrettyTable.horizontal_char = "─"
PrettyTable.bottom_left_junction_char = "└"
PrettyTable.bottom_right_junction_char = "┘"
PrettyTable.top_left_junction_char = "┌"
PrettyTable.top_right_junction_char = "┐"
PrettyTable.left_junction_char = "├"
PrettyTable.right_junction_char = "┤"
PrettyTable.top_junction_char = "┬"
PrettyTable.bottom_junction_char = "┴"
PrettyTable.junction_char = "┼"

@bot.event
async def setup_hook():
    for filename in os.listdir("Bot\Cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"Cogs.{filename[:-3]}")
            printex(f"Loaded Cogs: {filename[:-3]}")

@bot.event 
async def on_ready():
    ConnectToDatabase()
    printex(f"{bot.user.name} is activated.")
    try: # Sync all slash(/) commands. Must needed
        synced = await bot.tree.sync()
        printex(f"{bot.user.name} has synced {len(synced)} command(s)")
    except Exception as e:
        printex(f"I Cannot sync any command(s) because of {e}")

with open("B:/token.txt", "r") as file:
    token = file.readline()
bot.run(token= token, reconnect= True, log_handler= None)