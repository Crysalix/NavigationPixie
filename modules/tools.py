#!/usr/bin/env python3
import asyncio
import discord
import re

import config as cfg

from discord.ext import commands
from discord.utils import get
from pixie_function import *

import config as cfg

class Tools(commands.Cog, name="Tools"):

    def __init__(self, bot):
        self.bot = bot
        self.locales = readData('locales')
        self.owner = bot.get_user(cfg.bot_ownerid)

    def __unload(self):
        pass

    @commands.command()
    async def info(self, ctx):
        """Show info about the bot"""
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["tools"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            em = discord.Embed(title='A discord bot writen in Python3', type='rich', description='Bot info ', url='https://pixiebot.net', colour=0x7289da, timestamp=datetime.datetime.utcnow())
            em.set_author(name=ctx.me.name, icon_url=ctx.me.avatar_url)
            em.set_thumbnail(url=ctx.me.avatar_url)
            em.add_field(name=self.locales[lang]['tools']['messages']['guildcount'], value=len(self.bot.guilds))
            em.add_field(name=self.locales[lang]['tools']['messages']['membercount'], value=len(list(self.bot.get_all_members())))
            em.add_field(name='Links', value='[Github](https://github.com/Crysalix/NavigationPixie)')
            em.set_footer(text='By {0.display_name}#{0.discriminator}'.format(self.owner), icon_url=self.owner.avatar_url)
            await ctx.send(embed=em)

    @commands.command()
    async def userinfo(self, ctx, *args):
        """Show info about a given user"""
        serverlistmodules = readData('server', ctx.message.author.guild.id)
        if serverlistmodules["tools"]["last"] == "enabled":
            if args:
                try:
                    user = int(''.join(filter(str.isdigit, args[0])))
                    user = self.bot.get_user(user)
                    em = discord.Embed(title='', type='rich', description='User info', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                    em.set_author(name='{0.display_name}#{0.discriminator}'.format(user), icon_url=user.avatar_url)
                    em.set_thumbnail(url=user.avatar_url)
                    em.add_field(name='Bot ?', value=user.bot)
                    em.add_field(name='Created at', value=user.created_at)
                    em.set_footer(text='ID : {}'.format(user.id))
                    await ctx.send(embed=em)
                except:
                    await ctx.send('Bad ID or inexistant user (we must have a server in common).')
            else:
                await ctx.send('You need to tag an user.')

async def setup(bot):
    await bot.add_cog(Tools(bot))
