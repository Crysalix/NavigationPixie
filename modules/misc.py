#!/usr/bin/env python3.5
import asyncio
import discord
import json
import random
import time

import config as cfg

from discord.ext import commands
from pixie_function import *

class Misc:

    def __init__(self, bot):
        self.bot = bot
        self.locales = readData('locales')

    def __unload(self):
        pass

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong !"""
        if ctx.message.author == self.bot.user:
            return
        serverlistmodules = readData('server', ctx.message.author.server.id)
        if serverlistmodules["misc"]["last"] == "disabled":
            return
        await self.bot.send_typing(ctx.message.channel)
        await asyncio.sleep(0.5)
        await self.bot.say('Pong !')

    @commands.command(pass_context=True)
    async def excuse(self, ctx, rand=1):
        if ctx.message.author.id == cfg.bot_ownerid:
            count=0
            msg=''
            while True:
                ran = random.randrange(5)
                ran += 1
                if ran == 1:
                    msg=msg + '\n- Le démon s\'est échappé du pentagramme.'
                elif ran == 2:
                    msg=msg + '\n- Invasion d\'Elfes.'
                elif ran == 3:
                    msg=msg + '\n- Le dev code avec le cul.'
                elif ran == 4:
                    msg=msg + '\n- Les lutins sont en grève.'
                elif ran == 5:
                    msg=msg + '\n- Le chat s\'est couché sur le clavier.'
                count +=1
                if count == rand:
                    break
            await self.bot.say('**Excuses :** ' + msg)

    @commands.command(pass_context=True)
    async def flip(self, ctx):
        fail = random.randrange(100)
        serverlistmodules = readData('server', ctx.message.author.server.id)
        if serverlistmodules["misc"]["last"] == "disabled":
            return
        lang = serverlistmodules['bot']['config']['lang']['value']
        if fail == 0:
            await self.bot.say(self.locales[lang]['misc']['messages']['flipfail'])
        else:
            i = random.randrange(2)
            if i == 0:
                await self.bot.say('Pile !')
            elif i == 1:
                await self.bot.say('Face !')

    @commands.command(pass_context=True)
    async def roll(self, ctx):
        dice = random.randrange(6)
        dice += 1
        serverlistmodules = readData('server', ctx.message.author.server.id)
        if serverlistmodules["misc"]["last"] == "disabled":
            return
        await self.bot.say(dice)

    @commands.command(pass_context=True)
    async def rand(self, ctx, args0 = None):
        serverlistmodules = readData('server', ctx.message.author.server.id)
        if serverlistmodules["misc"]["last"] == "disabled":
            return
        lang = serverlistmodules['bot']['config']['lang']['value']
        try:
            ran = int(args0)
        except TypeError:#no arg specified
            await self.bot.say(self.locales[lang]['misc']['messages']['randnoarg'])
        except ValueError:#not an int
            await self.bot.say(self.locales[lang]['misc']['messages']['randnoarg'])
        else:
            if ran == 0:
                await self.bot.say(self.locales[lang]['misc']['messages']['randnozero'])
            elif ran == 1:
                await self.bot.say(self.locales[lang]['misc']['messages']['randone'])
            else:
                try:
                    rand = random.randrange(ran)
                except ValueError:
                    await self.bot.say(self.locales[lang]['misc']['messages']['randnotpos'])
                else:
                    rand += 1
                    await self.bot.say(rand)

    @commands.command(pass_context=True)
    async def ck(self, ctx):
        if ctx.message.author.id == cfg.bot_ownerid:
            rand = random.randrange(7)
            serverlistmodules = readData('server', ctx.message.author.server.id)
            if serverlistmodules["misc"]["last"] == "disabled":
                return
            if rand == 0:
                await self.bot.say('-tastrophique !')
            if rand == 1:
                await self.bot.say('-rément n\'importe quoi !')
            if rand == 2:
                await self.bot.say('-do !')
            if rand == 3:
                await self.bot.say('-ptivant !')
            if rand == 4:
                await self.bot.say('-ssé !')
            if rand == 5:
                await self.bot.say('-otique !')
            if rand == 6:
                await self.bot.say('-rricatural !')

    @commands.command(pass_context=True)
    async def say(self, ctx):
        if ctx.message.author.id == cfg.bot_ownerid:
            msg = ctx.message.content.split(" ", 1)[1]
            await self.bot.say(msg)

def setup(bot):
    bot.add_cog(Misc(bot))
