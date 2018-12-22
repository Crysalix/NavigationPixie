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

    def __unload(self):
        pass

    #BAN EVENT
    async def on_member_ban(member):
        serverlistmodules = readData('server', member.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
        embed = discord.Embed(description='Membre banni : <@' + member.id + '>', colour=0xFF0000, timestamp=datetime.datetime.utcnow())
        await self.bot.send_message(self.bot.get_channel(channel), embed=embed)

    async def on_member_unban(server, user):
        serverlistmodules = readData('server', user.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
        embed = discord.Embed(description='Membre débanni : <@' + user.id + '>', colour=0x00FF00, timestamp=datetime.datetime.utcnow())
        await self.bot.send_message(self.bot.get_channel(channel), embed=embed)

    #MESSAGES EVENT
    async def on_message_edit(self, before, after):
        if before.author.id == self.bot.user.id:
            return
        try:
            serverlistmodules = readData('server', before.author.server.id)
            if serverlistmodules["logging"]["last"] == "disabled":
                return
            if before.content != after.content:
                channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
                embed = discord.Embed(description='<@' + before.author.id + '> **dans** <#' + before.channel.id + '>\n**Avant** : ' + before.content + '\n**Après** : ' + after.content, colour=0xFF8000, timestamp=datetime.datetime.utcnow())
                await self.bot.send_message(self.bot.get_channel(channel), embed=embed)
        except AttributeError:
            #Webhook
            return

    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
        serverlistmodules = readData('server', message.author.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
        embed = discord.Embed(description='<@' + message.author.id + '> **dans** <#' + message.channel.id + '>\n**Supprimé** : ' + message.content, colour=0xFF0000, timestamp=datetime.datetime.utcnow())
        await self.bot.send_message(self.bot.get_channel(channel), embed=embed)

    #REACTIONS EVENT
    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', user.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
        fmt = '`{0.emoji}`'
        embed = discord.Embed(description='Reaction added (`' + fmt.format(reaction) + '`) by <@' + user.id + '> on https://discordapp.com/channels/' + user.server.id + '/' + reaction.message.channel.id + '/' + reaction.message.id, colour=0x00FF00, timestamp=datetime.datetime.utcnow())
        await self.bot.send_message(self.bot.get_channel(channel), embed=embed)

    async def on_reaction_remove(self, reaction, user):
        if user.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', user.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
        fmt = '`{0.emoji}`'
        embed = discord.Embed(description='Reaction removed (' + fmt.format(reaction) + ') by <@' + user.id + '> on https://discordapp.com/channels/' + user.server.id + '/' + reaction.message.channel.id + '/' + reaction.message.id, colour=0x00FF00)
        await self.bot.send_message(self.bot.get_channel(channel), embed=embed)

    async def on_reaction_clear(self, message, reactions):
        if message.author.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', message.author.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
        fmt = 'Reaction Cleared on message from <@{0.author.id}> : {0.content}\n```{1}```'
        await self.bot.send_message(self.bot.get_channel(channel), fmt.format(message, reactions))

    #CHANNELS EVENT
    async def on_channel_create(self, chan):
        serverlistmodules = readData('server', chan.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
        fmt = 'Channel créé : <#{0.id}>'
        await self.bot.send_message(self.bot.get_channel(channel), fmt.format(chan))

    async def on_channel_delete(self, chan):
        serverlistmodules = readData('server', chan.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
        fmt = 'Channel supprimé : #{0.name}'
        await self.bot.send_message(self.bot.get_channel(channel), fmt.format(chan))

    async def on_channel_update(self, before, after):
        serverlistmodules = readData('server', before.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        if before.name != after.name:
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = 'Channel édité : #{0.name} -> <#{1.id}>'
            await self.bot.send_message(self.bot.get_channel(channel), fmt.format(before, after))

    #MEMBERS EVENT
    async def on_member_update(self, before, after):
        if before.id == self.bot.user.id:
            return
        serverlistmodules = readData('server', before.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        if before.nick != after.nick:
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
            fmt = 'Nick update : {0.nick} -> {1.nick}.'
            await self.bot.send_message(self.bot.get_channel(channel), fmt.format(before, after))

    async def on_member_remove(self, member):
        serverlistmodules = readData('server', member.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['modlog_chan']['value'])))
        embed = discord.Embed(description='Membre parti : ' + member.name + '.', colour=0xFF8000, timestamp=datetime.datetime.utcnow())
        await self.bot.send_message(self.bot.get_channel(channel), embed=embed)
            
    #SERVER EVENT
    async def on_server_update(self, before, after):
        serverlistmodules = readData('server', before.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
        fmt = '**Server Update**\n```Name : {0.name} -> {1.name}\nTimeout : {0.afk_timeout} -> {1.afk_timeout}\nAfk Channel : {0.afk_channel} -> {1.afk_channel}```'
        await self.bot.send_message(self.bot.get_channel(channel), fmt.format(before, after))

    async def on_server_role_create(self, role):
        serverlistmodules = readData('server', role.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
        fmt = '**Role created**\n```New role : {0}```'
        await self.bot.send_message(self.bot.get_channel(channel), fmt.format(role))

    async def on_server_role_delete(self, role):
        serverlistmodules = readData('server', role.server.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
        fmt = '**Role deleted**\n```Role deleted : {0}```'
        await self.bot.send_message(self.bot.get_channel(channel), fmt.format(role))

    async def on_server_role_update(self, before, after):
        serverlistmodules = readData('server', before.id)
        if serverlistmodules["logging"]["last"] == "disabled":
            return
        if before.name != after.name:
            channel = str(''.join(filter(str.isdigit, serverlistmodules['logging']['config']['adminlog_chan']['value'])))
            fmt = '**Role updated**\n```{0.name} -> {1.name}```'
            await self.bot.send_message(self.bot.get_channel(channel), fmt.format(before, after))

def setup(bot):
    bot.add_cog(Logging(bot))
