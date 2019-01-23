#!/usr/bin/env python3.5
import asyncio
import discord
import random

from discord.ext import commands
from discord.utils import get
from pixie_function import *

class Games:

    def __init__(self, bot):

        async def randomGames(self):
            while True:
                serverCount = len(self.bot.guilds)
                memberCount = len(list(self.bot.get_all_members()))
                name, type = random.choice(list(gameslist.items()))
                #await self.bot.change_presence(activity=discord.Game(name=randomGame.format(guilds = serverCount, members = memberCount)))
                await self.bot.change_presence(activity=discord.Activity(type=type, name=name.format(guilds = serverCount, members = memberCount)))
                #await bot.change_presence(activity=discord.Activity(type=watching, name='Trash Animes'.format(guilds = guildCount, members = memberCount)))
                await asyncio.sleep(300) # 5 minutes

        self.bot = bot
        self.bot.task = self.bot.loop.create_task(randomGames(self))

    def __unload(self):
        self.bot.task.cancel()

gameslist = {
    "Sword Art Online !": "3",
    "ALfheim Online !": "3",
    "Gun Gale Online !": "3",
    "Monitoring players healt": "3",
    "with Cats": "0",
    "pixiebot.net | try !help": "0",
    "with Python": "0",
    "with async": "0",
    "on {guilds:d} Servers": "2",
    "with {members:d} Members": "0"
}

def setup(bot):
    bot.add_cog(Games(bot))
    
