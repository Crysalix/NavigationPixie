#!/usr/bin/env python3.5
import asyncio
import discord
import random

import config as cfg

from discord.ext import commands
from pixie_function import *

class Misc:

    def __init__(self, bot):
        self.bot = bot
        self.locales = readData('locales')

    def __unload(self):
        pass

    @commands.command()
    async def ping(self, ctx):
        """Pong !"""
        # if ctx.message.author == self.bot.user:
            # return
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["misc"]["last"] == "enabled":
            chan = ctx.message.channel
            async with chan.typing():
                await asyncio.sleep(0.5)
                await chan.send('Pong !')

    @commands.command()
    async def excuse(self, ctx, rand=1):
        if ctx.message.author.id == cfg.bot_ownerid:
            chan = ctx.message.channel
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
            await chan.send('**Excuses :** ' + msg)

    @commands.command()
    async def flip(self, ctx):
        fail = random.randrange(100)
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["misc"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            chan = ctx.message.channel
            if fail == 0:
                await chan.send(self.locales[lang]['misc']['messages']['flipfail'])
            else:
                i = random.randrange(2)
                if i == 0:
                    await chan.send('Pile !')
                elif i == 1:
                    await chan.send('Face !')

    @commands.command()
    async def roll(self, ctx):
        dice = random.randrange(6)
        dice += 1
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["misc"]["last"] == "enabled":
            chan = ctx.message.channel
            await chan.send(dice)

    @commands.command()
    async def rand(self, ctx, args0 = None):
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["misc"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            chan = ctx.message.channel
            try:
                ran = int(args0)
            except TypeError:#no arg specified
                await chan.send(self.locales[lang]['misc']['messages']['randnoarg'])
            except ValueError:#not an int
                await chan.send(self.locales[lang]['misc']['messages']['randnoarg'])
            else:
                if ran == 0:
                    await chan.send(self.locales[lang]['misc']['messages']['randnozero'])
                elif ran == 1:
                    await chan.send(self.locales[lang]['misc']['messages']['randone'])
                else:
                    try:
                        rand = random.randrange(ran)
                    except ValueError:
                        await chan.send(self.locales[lang]['misc']['messages']['randnotpos'])
                    else:
                        rand += 1
                        await chan.send(rand)

    @commands.command()
    async def hey(self, ctx):
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["misc"]["last"] == "enabled":
            rand = random.randrange(3)
            chan = ctx.message.channel
            if rand == 0:
                await chan.send('Listen !')
            if rand == 1:
                await chan.send('Hooo')
            if rand == 2:
                await chan.send('<@{}> Wake up !'.format(ctx.message.author.id))

    @commands.command()
    async def ck(self, ctx):
        if ctx.message.author.id == cfg.bot_ownerid:
            rand = random.randrange(7)
            serverlistmodules = readData('server', ctx.message.author.guild.id)
            if serverlistmodules["misc"]["last"] == "enabled":
                chan = ctx.message.channel
                if rand == 0:
                    await chan.send('-tastrophique !')
                if rand == 1:
                    await chan.send('-rément n\'importe quoi !')
                if rand == 2:
                    await chan.send('-do !')
                if rand == 3:
                    await chan.send('-ptivant !')
                if rand == 4:
                    await chan.send('-ssé !')
                if rand == 5:
                    await chan.send('-otique !')
                if rand == 6:
                    await chan.send('-rricatural !')

    @commands.command()
    async def say(self, ctx):
        if ctx.message.author.id == cfg.bot_ownerid:
            msg = ctx.message.content.split(" ", 1)[1]
            chan = ctx.message.channel
            await chan.send(msg)

def setup(bot):
    bot.add_cog(Misc(bot))
