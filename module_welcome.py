#!/usr/bin/env python3.5
import asyncio
import time
import discord

from discord.ext import commands
from pixie_function import *

import config as cfg

class Welcome:

    def __init__(self, bot):
        self.bot = bot

    def __unload(self):
        pass

    async def on_member_join(self, member):
        serverlistmodules = readData('server', member.server.id)
        if serverlistmodules["welcome"]["last"] == "disabled":
            return
        fmt = serverlistmodules['welcome']['config']['message']['value']
        channel = str(''.join(filter(str.isdigit, serverlistmodules['welcome']['config']['channel']['value'])))
        member.id = '<@' + member.id + '>'
        await self.bot.send_message(self.bot.get_channel(channel), fmt.format(user=member.id))

def setup(bot):
    bot.add_cog(Welcome(bot))
