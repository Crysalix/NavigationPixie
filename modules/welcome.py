#!/usr/bin/env python3.5
import asyncio
import discord

from discord.ext import commands
from pixie_function import *

class Welcome(commands.Cog, name="Welcome"):

    def __init__(self, bot):
        self.bot = bot

    def __unload(self):
        pass

    async def on_member_join(self, member):
        serverlistmodules = readData('server', member.guild.id)
        if serverlistmodules["welcome"]["last"] == "enabled":
            fmt = serverlistmodules['welcome']['config']['joinmsg']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['welcome']['config']['channel']['value'])))
            userid = '<@{}>'.format(member.id)
            await self.bot.get_channel(int(channel)).send(fmt.format(user=userid))

    async def on_member_remove(self, member):
        serverlistmodules = readData('server', member.guild.id)
        if serverlistmodules["welcome"]["last"] == "enabled":
            fmt = serverlistmodules['welcome']['config']['leavemsg']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['welcome']['config']['channel']['value'])))
            await self.bot.get_channel(int(channel)).send(fmt.format(user=member.name))

def setup(bot):
    bot.add_cog(Welcome(bot))
