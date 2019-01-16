#!/usr/bin/env python3.5
import asyncio
import discord
import random
import time

from discord.ext import commands
from pixie_function import *

import config as cfg

class Logging:

    def __init__(self, bot):
        self.bot = bot
        self.locales = readData('locales')

    def __unload(self):
        pass

    #BAN EVENT
    async def on_member_ban(member):
        serverlistmodules = readData('server', member.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            embed = discord.Embed(description=self.locales[lang]['logging']['messages']['on_member_ban'].format(member.id), colour=0xFF0000, timestamp=datetime.datetime.utcnow())
            await self.bot.send_message(self.bot.get_channel(channel), embed=embed)

    async def on_member_unban(server, user):
        serverlistmodules = readData('server', user.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            embed = discord.Embed(description=self.locales[lang]['logging']['messages']['on_member_unban'].format(user.id), colour=0x00FF00, timestamp=datetime.datetime.utcnow())
            await self.bot.send_message(self.bot.get_channel(channel), embed=embed)

    #MESSAGES EVENT
    async def on_message_edit(self, before, after):
        if before.author.id == self.bot.user.id:
            return
        try:
            serverlistmodules = readData('server', before.author.server.id)
            if serverlistmodules["logging"]["last"] == "enabled":
                lang = serverlistmodules['bot']['config']['lang']['value']
                if before.content != after.content:
                    channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
                    fmt = self.locales[lang]['logging']['messages']['on_message_edit']
                    embed = discord.Embed(description=fmt.format(before.author.id, before.channel.id, before.content, after.content), colour=0xFF8000, timestamp=datetime.datetime.utcnow())
                    await self.bot.send_message(self.bot.get_channel(channel), embed=embed)
        except AttributeError:
            #Webhook
            return

    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
        serverlistmodules = readData('server', message.author.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_message_delete']
            embed = discord.Embed(description=fmt.format(message.author.id, message.channel.id, message.content), colour=0xFF0000, timestamp=datetime.datetime.utcnow())
            await self.bot.send_message(self.bot.get_channel(channel), embed=embed)

    #REACTIONS EVENT
    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', user.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_reaction_add']
            embed = discord.Embed(description=fmt.format(reaction.emoji, user.id, user.server.id, reaction.message.channel.id, reaction.message.id), colour=0x00FF00, timestamp=datetime.datetime.utcnow())
            await self.bot.send_message(self.bot.get_channel(channel), embed=embed)

    async def on_reaction_remove(self, reaction, user):
        if user.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', user.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_reaction_remove']
            embed = discord.Embed(description=fmt.format(reaction.emoji, user.id, user.server.id, reaction.message.channel.id, reaction.message.id), colour=0x00FF00, timestamp=datetime.datetime.utcnow())
            await self.bot.send_message(self.bot.get_channel(channel), embed=embed)

    async def on_reaction_clear(self, message, reactions):
        return # Not working 
        if message.author.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', message.author.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_reaction_clear']
            await self.bot.send_message(self.bot.get_channel(channel), fmt.format(message.author.id, reactions, user.server.id, reaction.message.channel.id, reaction.message.id))

    #CHANNELS EVENT
    async def on_channel_create(self, chan):
        serverlistmodules = readData('server', chan.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_channel_create']
            await self.bot.send_message(self.bot.get_channel(channel), fmt.format(chan.id))

    async def on_channel_delete(self, chan):
        serverlistmodules = readData('server', chan.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_channel_delete']
            await self.bot.send_message(self.bot.get_channel(channel), fmt.format(chan.name))

    async def on_channel_update(self, before, after):
        serverlistmodules = readData('server', before.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            if before.name != after.name:
                lang = serverlistmodules['bot']['config']['lang']['value']
                channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
                fmt = self.locales[lang]['logging']['messages']['on_channel_update']
                await self.bot.send_message(self.bot.get_channel(channel), fmt.format(before.name, after.id))

    #MEMBERS EVENT
    async def on_member_update(self, before, after):
        if before.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', before.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            if before.nick != after.nick:
                lang = serverlistmodules['bot']['config']['lang']['value']
                channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
                fmt = self.locales[lang]['logging']['messages']['on_member_update']
                await self.bot.send_message(self.bot.get_channel(channel), fmt.format(before.nick, after.nick))

    async def on_member_remove(self, member):
        serverlistmodules = readData('server', member.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_member_remove']
            embed = discord.Embed(description=fmt.format(member.name), colour=0xFF8000, timestamp=datetime.datetime.utcnow())
            await self.bot.send_message(self.bot.get_channel(channel), embed=embed)
            
    #SERVER EVENT
    async def on_server_update(self, before, after):
        serverlistmodules = readData('server', before.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_server_update']
            await self.bot.send_message(self.bot.get_channel(channel), fmt.format(before, after))

    async def on_server_role_create(self, role):
        serverlistmodules = readData('server', role.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_server_role_create']
            await self.bot.send_message(self.bot.get_channel(channel), fmt.format(role))

    async def on_server_role_delete(self, role):
        serverlistmodules = readData('server', role.server.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            lang = serverlistmodules['bot']['config']['lang']['value']
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = self.locales[lang]['logging']['messages']['on_server_role_delete']
            await self.bot.send_message(self.bot.get_channel(channel), fmt.format(role))

    async def on_server_role_update(self, before, after):
        serverlistmodules = readData('server', before.id)
        if serverlistmodules["logging"]["last"] == "enabled":
            if before.name != after.name:
                lang = serverlistmodules['bot']['config']['lang']['value']
                channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
                fmt = self.locales[lang]['logging']['messages']['on_server_role_update']
                await self.bot.send_message(self.bot.get_channel(channel), fmt.format(before, after))

def setup(bot):
    bot.add_cog(Logging(bot))
