#!/usr/bin/env python3
import asyncio
import datetime
import discord

from discord.ext import commands
from pixie_function import *

import config as cfg

class Logging(commands.Cog, name="Logging"):

    def __init__(self, bot):
        self.bot = bot
        self.locales = readData('locales')

    def __unload(self):
        pass

    #BAN EVENT
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        serverlistmodules = readData('server', member.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            embed = discord.Embed(description=self.locales[lang]['logging']['messages']['on_member_ban'].format(member.id), colour=0xFF0000, timestamp=datetime.datetime.utcnow())
            await self.bot.get_channel(int(channel)).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        serverlistmodules = readData('server', guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            embed = discord.Embed(description=self.locales[lang]['logging']['messages']['on_member_unban'].format(user.id), colour=0x00FF00, timestamp=datetime.datetime.utcnow())
            await self.bot.get_channel(int(channel)).send(embed=embed)

    #MESSAGES EVENT
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.id == self.bot.user.id:
            return
        try:
            serverlistmodules = readData('server', before.author.guild.id)
            if serverlistmodules["logging"]["last"] == "enabled":
                lang = serverlistmodules['bot']['config']['lang']['value']
                if before.content != after.content:
                    channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
                    fmt = self.locales[lang]['logging']['messages']['on_message_edit']
                    embed = discord.Embed(description=fmt.format(before.author.id, before.channel.id, before.content, after.content), colour=0xFF8000, timestamp=datetime.datetime.utcnow())
                    await self.bot.get_channel(int(channel)).send(embed=embed)
        except AttributeError:
            #Webhook
            return

    # async def on_raw_message_delete(self, payload):
        # serverlistmodules = readData('server', payload.guild_id)
        # if serverlistmodules["logging"]["last"] == "enabled":
            # lang = serverlistmodules['bot']['config']['lang']['value']
            # channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            # fmt = self.locales[lang]['logging']['messages']['on_message_delete']
            # message = self.bot.get_message(payload.message_id)
            # embed = discord.Embed(description=fmt.format(message.author.id, payload.channel_id, message.content), colour=0xFF0000, timestamp=datetime.datetime.utcnow())
            # await self.bot.get_channel(int(channel)).send(embed=embed)
            
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
        serverlistmodules = readData('server', message.author.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_message_delete']
            embed = discord.Embed(description=fmt.format(message.author.id, message.channel.id, message.content), colour=0xFF0000, timestamp=datetime.datetime.utcnow())
            await self.bot.get_channel(int(channel)).send(embed=embed)

    #REACTIONS EVENT
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', user.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_reaction_add']
            embed = discord.Embed(description=fmt.format(reaction.emoji, user.id, user.guild.id, reaction.message.channel.id, reaction.message.id), colour=0x00FF00, timestamp=datetime.datetime.utcnow())
            await self.bot.get_channel(int(channel)).send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', user.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_reaction_remove']
            embed = discord.Embed(description=fmt.format(reaction.emoji, user.id, user.guild.id, reaction.message.channel.id, reaction.message.id), colour=0x00FF00, timestamp=datetime.datetime.utcnow())
            await self.bot.get_channel(int(channel)).send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        return # Not working 
        if message.author.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', message.author.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_reaction_clear']
            await self.bot.get_channel(int(channel)).send(fmt.format(message.author.id, reactions, user.guild.id, reaction.message.channel.id, reaction.message.id))

    #CHANNELS EVENT
    @commands.Cog.listener()
    async def on_guild_channel_create(self, chan):
        serverlistmodules = readData('server', chan.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_channel_create']
            await self.bot.get_channel(int(channel)).send(fmt.format(chan.id))

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, chan):
        serverlistmodules = readData('server', chan.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_channel_delete']
            await self.bot.get_channel(int(channel)).send(fmt.format(chan.name))

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        serverlistmodules = readData('server', before.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            if before.name != after.name:
                lang = serverlistmodules['bot']['config']['lang']['value']
                channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
                fmt = self.locales[lang]['logging']['messages']['on_channel_update']
                await self.bot.get_channel(int(channel)).send(fmt.format(before.name, after.id))

    #MEMBERS EVENT
    @commands.Cog.listener()
    async def on_member_join(self, member):
        serverlistmodules = readData('server', member.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            embed = discord.Embed(description='New member : <@{}>'.format(member.id), colour=0x00FF00)
            await self.bot.get_channel(int(channel)).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', before.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            if before.nick != after.nick:
                lang = serverlistmodules['bot']['config']['lang']['value']
                channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
                fmt = self.locales[lang]['logging']['messages']['on_member_update']
                await self.bot.get_channel(int(channel)).send(fmt.format(before.nick, after.nick))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        serverlistmodules = readData('server', member.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_member_remove']
            embed = discord.Embed(description=fmt.format(member.name), colour=0xFF8000, timestamp=datetime.datetime.utcnow())
            await self.bot.get_channel(int(channel)).send(embed=embed)

    #SERVER EVENT
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        serverlistmodules = readData('server', before.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_server_update']
            await self.bot.get_channel(int(channel)).send(fmt.format(before, after))

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        serverlistmodules = readData('server', role.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_server_role_create']
            await self.bot.get_channel(int(channel)).send(fmt.format(role))

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        serverlistmodules = readData('server', role.guild.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_server_role_delete']
            await self.bot.get_channel(int(channel)).send(fmt.format(role))

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        serverlistmodules = readData('server', before.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            #if before.name != after.name:
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_server_role_update']
            embed = discord.Embed(description='Role update', colour=0xFF8000, timestamp=datetime.datetime.utcnow())
            embed.add_field(name='Name :', value=fmt.format(before, after))
            embed.set_footer(text=before.id)
            await self.bot.get_channel(int(channel)).send(embed=embed)

def setup(bot):
    bot.add_cog(Logging(bot))
