#!/usr/bin/env python3
import asyncio
import discord
import random

import config as cfg

from discord.ext import commands
from pixie_function import *

class Misc(commands.Cog, name="Misc"):

    def __init__(self, bot):
        self.bot = bot
        self.locales = readData('locales')

    def __unload(self):
        pass

    @commands.command()
    async def ping(self, ctx):
        """Pong !"""
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["misc"]["last"] == "enabled":
            async with ctx.typing():
                await asyncio.sleep(0.5)
                await ctx.send('Pong !')

    @commands.command()
    async def excuse(self, ctx, rand=1):
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
        await ctx.send('**Excuses :** ' + msg)

    @commands.command()
    async def flip(self, ctx):
        fail = random.randrange(100)
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["misc"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            if fail == 0:
                await ctx.send(self.locales[lang]['misc']['messages']['flipfail'])
            else:
                i = random.randrange(2)
                if i == 0:
                    await ctx.send('<@{}> Pile !'.format(ctx.message.author.id))
                elif i == 1:
                    await ctx.send('<@{}> Face !'.format(ctx.message.author.id))

    @commands.command()
    async def roll(self, ctx):
        dice = random.randrange(6)
        dice += 1
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["misc"]["last"] == "enabled":
            await ctx.send(dice)

    @commands.command()
    async def rand(self, ctx, args0 = None):
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["misc"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            try:
                ran = int(args0)
            except TypeError:#no arg specified
                await ctx.send(self.locales[lang]['misc']['messages']['randnoarg'])
            except ValueError:#not an int
                await ctx.send(self.locales[lang]['misc']['messages']['randnoarg'])
            else:
                if ran == 0:
                    await ctx.send(self.locales[lang]['misc']['messages']['randnozero'])
                elif ran == 1:
                    await ctx.send(self.locales[lang]['misc']['messages']['randone'])
                else:
                    try:
                        rand = random.randrange(ran)
                    except ValueError:
                        await ctx.send(self.locales[lang]['misc']['messages']['randnotpos'])
                    else:
                        rand += 1
                        await ctx.send(rand)

    @commands.command()
    async def hey(self, ctx):
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["misc"]["last"] == "enabled":
            rand = random.randrange(3)
            if rand == 0:
                await ctx.send('Listen !')
            elif rand == 1:
                await ctx.send('Hooo')
            elif rand == 2:
                await ctx.send('<@{}> Wake up !'.format(ctx.message.author.id))

    @commands.command()
    async def ck(self, ctx):
        if ctx.message.author.id == cfg.bot_ownerid:
            rand = random.randrange(7)
            serverlistmodules = readData('server', ctx.message.author.guild.id)
            if serverlistmodules["misc"]["last"] == "enabled":
                if rand == 0:
                    await ctx.send('-tastrophique !')
                elif rand == 1:
                    await ctx.send('-rément n\'importe quoi !')
                elif rand == 2:
                    await ctx.send('-do !')
                elif rand == 3:
                    await ctx.send('-ptivant !')
                elif rand == 4:
                    await ctx.send('-ssé !')
                elif rand == 5:
                    await ctx.send('-otique !')
                elif rand == 6:
                    await ctx.send('-rricatural !')

    @commands.command()
    async def say(self, ctx):
        if ctx.message.author.id == cfg.bot_ownerid:
            msg = ctx.message.content.split(" ", 1)[1]
            await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(Misc(bot))
