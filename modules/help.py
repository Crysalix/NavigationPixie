#!/usr/bin/env python3
import asyncio
import datetime
import discord

from discord.ext import commands
from pixie_function import *

import config as cfg

class Help(commands.Cog, name="Help"):

    def __init__(self, bot):
        self.bot = bot
        self.locales = readData('locales')

    def __unload(self):
        pass

    @commands.command()
    async def help(self, ctx):
        """Help message generator."""
        listmodules = readData('main')
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        lang = serverlistmodules['bot']['config']['lang']['value']
        if ctx.message.author == self.bot.user:
            return
        # botmaster help command
        if ctx.message.author.id == cfg.bot_ownerid and ctx.message.channel.id == cfg.botlog_chan:
            embed = discord.Embed(description=':gear: Botmaster Commands list :', colour=0x7289da, timestamp=datetime.datetime.utcnow())
            embed.add_field(name='!load', value='Load bot modules.', inline=False)
            embed.add_field(name='!unload', value='Unload bot modules.', inline=False)
            embed.add_field(name='!reload', value='Reload given bot modules or all.', inline=False)
            embed.add_field(name='!checkmodule', value='Check modules parsing.', inline=False)
            embed.add_field(name='!quit', value='Close connexion and stop bot instance.', inline=False)
            await ctx.send(embed=embed)
        # server admin help command
        if ctx.message.author.id == ctx.message.author.guild.owner.id:
            embed = discord.Embed(description=':gear: Admin Commands list :', colour=0x7289da, timestamp=datetime.datetime.utcnow())
            embed.add_field(name='!enable', value=self.locales[lang]['core']['commands']['enable'], inline=False)
            embed.add_field(name='!disable', value=self.locales[lang]['core']['commands']['disable'], inline=False)
            embed.add_field(name='!config', value=self.locales[lang]['core']['commands']['config'], inline=False)
            embed.add_field(name='!checkconfig', value=self.locales[lang]['core']['commands']['checkconfig'], inline=False)
            await ctx.send(embed=embed)
        # admin/mod help command
        # regular help command
        embed = discord.Embed(description=':gear: Commands list :', colour=0x7289da, timestamp=datetime.datetime.utcnow())
        if (listmodules["help"]["last"] == "loaded" and serverlistmodules["help"]["last"] == "enabled"):
            embed.add_field(name='!help', value=self.locales[lang]['help']['commands']['help'], inline=False)
        if (listmodules["misc"]["last"] == "loaded" and serverlistmodules["misc"]["last"] == "enabled"):
            embed.add_field(name='!excuse [num]', value=self.locales[lang]['misc']['commands']['excuse'], inline=False)
            embed.add_field(name='!flip', value=self.locales[lang]['misc']['commands']['flip'], inline=False)
            embed.add_field(name='!ping', value='Pong !', inline=False)
            embed.add_field(name='!rand', value=self.locales[lang]['misc']['commands']['rand'], inline=False)
            embed.add_field(name='!roll', value=self.locales[lang]['misc']['commands']['roll'], inline=False)
        if (listmodules["jokes"]["last"] == "loaded" and serverlistmodules["jokes"]["last"] == "enabled"):
            embed.add_field(name='!joke', value=self.locales[lang]['jokes']['commands']['joke'], inline=False)
        if (listmodules["poll"]["last"] == "loaded" and serverlistmodules["poll"]["last"] == "enabled"):
            embed.add_field(name='!poll', value=self.locales[lang]['poll']['commands']['poll'], inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
