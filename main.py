
import discord
#import keep_alive
import os
import json
import asyncio
import random
from discord.ext import commands
import sqlite3
import time 


conn = sqlite3.connect('bank.db')
cursorObj = conn.cursor()

intents = discord.Intents.default()
intents.members=True
token = 'token here'

#keep_alive.keep_alive()

description = '''Currency Bot'''


bot = commands.Bot(command_prefix='-', description=description, intents=intents)
#client = discord.Client(intents=intents)
bot.load_extension("cogs.currency")

@bot.command(hidden=True)
async def load(ctx, *, module):
    if ctx.author.id==386837370466598914:
        bot.load_extension(f"cogs.{module}")
        print(f"Loaded {module}")

@bot.command(hidden=True)
async def unload(ctx, *, module):
    if ctx.author.id==386837370466598914:
        bot.unload_extension(f"cogs.{module}")
        print(f"Unloaded {module}")

@bot.event
async def on_member_join(member):
    await make_bank(str(member.id))

@bot.command(hidden=True)
async def reload(ctx, *, module):
    if ctx.author.id==386837370466598914:
        bot.unload_extension(f"cogs.{module}")
        bot.load_extension(f"cogs.{module}")
        print(f"Reloaded {module}")

amounts = {}
#bot.load_extension("cogs.currency")

bot.run("token here")


