#!/usr/bin/env python3.5
import aiohttp
import asyncio
import datetime
import discord
import json
import logging
import random
import subprocess
import time
import traceback
import websockets
import sys

from discord.ext import commands
from discord.utils import get
from pixie_function import *

import config as cfg
import backoff

listmodules = readData('main')

bot = commands.Bot(command_prefix='!', description='Navigation Pixie')
bot.remove_command('help')

async def keep_running(client, token):
    retry = backoff.ExponentialBackoff()
    logging.info('DEBUG KEEP RUNNING')
    while True:
        try:
            await client.login(token)
        except (discord.HTTPException, aiohttp.ClientError):
            logging.exception("Discord.py pls login")
            await asyncio.sleep(retry.delay())
        else:
            break
    while client.is_logged_in:
        logging.info('while client.is_logged_in')
        if client.is_closed:
            client._closed.clear()
            client.http.recreate()
        try:
            await client.connect()
        except (discord.HTTPException, aiohttp.ClientError,
                discord.GatewayNotFound, discord.ConnectionClosed,
                websockets.InvalidHandshake,
                websockets.WebSocketProtocolError) as e:
            if isinstance(e, discord.ConnectionClosed) and e.code == 4004:
                raise # Do not reconnect on authentication failure
            logging.exception("Discord.py pls keep running")
            await asyncio.sleep(retry.delay())

@bot.event
async def on_ready():
    logging.info('NAVIGATIONPIXIE > Logged in as ' + bot.user.name + ' with ID ' + bot.user.id)
    #await bot.change_presence(activity=discord.Activity(type=watching, name='Trash Animes'.format(guilds = guildCount, members = memberCount)))
    await bot.change_presence(game=discord.Game(name='Sword Art online !'))
    await bot.send_message(bot.get_channel(cfg.botlog_chan), 'Connected ! Loading modules...')
    #Loading core module first
    try:
        bot.load_extension('module_core')
    except ImportError:
        await bot.send_message(bot.get_channel(cfg.botlog_chan), '<@258418027844993024> Failed to load core module ! Can\'t init bot instance !')
        logging.error('NAVIGATIONPIXIE > Failed to load core module ! Can\'t init bot instance !')
        await bot.close()
        sys.exit()
    except SyntaxError:
        if module == 'core':
            await bot.send_message(bot.get_channel(cfg.botlog_chan), '<@258418027844993024> Syntax error on core module ! Can\'t init bot instance !')
            logging.error('NAVIGATIONPIXIE > Syntax error on core module ! Can\'t init bot instance !')
            await bot.close()
            sys.exit()
    #Loading modules
    for module in listmodules:
        if listmodules[module]["default"] == "loaded":
            try:
                bot.load_extension('module_' + module)
            except ImportError:
                await bot.send_message(bot.get_channel(cfg.botlog_chan), '```' + traceback.format_exc() + '```')
                logging.error('NAVIGATIONPIXIE > Failed to load module ' + module + '.')
            except SyntaxError:
                await bot.send_message(bot.get_channel(cfg.botlog_chan), '```' + traceback.format_exc() + '```')
                logging.warning('NAVIGATIONPIXIE > Bad module : ' + module)
    await bot.send_message(bot.get_channel(cfg.botlog_chan), 'Ready !')
    logging.info('NAVIGATIONPIXIE > Connected !')

@bot.event
async def on_resumed():
   logging.warning('NAVIGATIONPIXIE > Session resumed...')

@bot.event
async def on_command_error(error, *args, **kwargs):
    ctx = args[0]
    if not str(error) == 'Command "' + ctx.invoked_with + '" is not found':
        await bot.send_message(bot.get_channel(cfg.botlog_chan), '<@258418027844993024>')
        embed = discord.Embed(title=':x: Command Error', colour=0x992d22, timestamp=datetime.datetime.utcnow())
        embed.description = '```py\n%s\n```' % traceback.format_exc()
        embed.add_field(name='Error', value=error)
        embed.add_field(name='Server', value=ctx.message.server.name)
        embed.add_field(name='Channel', value='<#' + ctx.message.channel.id + '>')
        embed.add_field(name='User', value='<@' + ctx.message.author.id + '>')
        embed.add_field(name='Command', value='`' + ctx.message.clean_content + '`')
        await bot.send_message(bot.get_channel(cfg.botlog_chan), embed=embed)

@bot.event
async def on_error(event, *args, **kwargs):
    await bot.send_message(bot.get_channel(cfg.botlog_chan), '<@258418027844993024>')
    embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c, timestamp=datetime.datetime.utcnow())
    embed.description = '```py\n%s\n```' % traceback.format_exc()
    embed.add_field(name='Event', value=event)
    await bot.send_message(bot.get_channel(cfg.botlog_chan), embed=embed)

#MISC
@bot.command(pass_context=True)
async def restart(ctx):
    if ctx.message.author.id == '258418027844993024':
        logging.info('NAVIGATIONPIXIE > Restart')
        await bot.say('I`ll be back !')
        await bot.close()

@bot.command(pass_context=True)
async def quit(ctx):
    if ctx.message.author.id == '258418027844993024':
        logging.info('NAVIGATIONPIXIE > SystemExit')
        await bot.say('Goodbye !')
        await bot.close()
        sys.exit()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        logging.info(message.server.name + ' > ' + message.content)
    if bot.user.mentioned_in(message):
        try:
            emoji = get(bot.get_all_emojis(), name='mention')
            await bot.add_reaction(message, emoji)
        except:
            print(traceback.format_exc())
    await bot.process_commands(message)

@bot.event
async def on_server_join(server):
    em = discord.Embed(title=server.name, type='rich', description='Total : ' + str(len(bot.servers)), colour=0x23d160, timestamp=datetime.datetime.utcnow())
    em.set_author(name='New server joined !', icon_url=server.icon_url)
    em.set_thumbnail(url=server.icon_url)
    em.add_field(name='ID', value=server.id)
    em.add_field(name='Region', value=server.region)
    em.add_field(name='Owner', value='<@' + server.owner.id + '>')
    em.add_field(name='Members', value=server.member_count)
    em.add_field(name='Created at', value=server.created_at)
    roles = ''
    for e in server.role_hierarchy:
        roles = roles + e.name + ' '
    em.add_field(name='Roles', value=roles)
    em.add_field(name='2FA', value=server.mfa_level)
    await bot.send_message(bot.get_channel(cfg.botlog_chan), embed=em)

@bot.event
async def on_server_remove(server):
    em = discord.Embed(title=server.name, type='rich', description='Total : ' + str(len(bot.servers)), colour=0xe74c3c, timestamp=datetime.datetime.utcnow())
    em.set_author(name='Server removed !', icon_url=server.icon_url)
    em.set_thumbnail(url=server.icon_url)
    em.add_field(name='ID', value=server.id)
    em.add_field(name='Region', value=server.region)
    em.add_field(name='Owner', value='<@' + server.owner.id + '>')
    em.add_field(name='Members', value=server.member_count)
    em.add_field(name='Created at', value=server.created_at)
    em.add_field(name='2FA', value=server.mfa_level)
    await bot.send_message(bot.get_channel(cfg.botlog_chan), embed=em)

logging.basicConfig(format='%(asctime)s | [%(levelname)s] | %(message)s', datefmt='%m/%d/%Y - %H:%M:%S', filename='latest.log',level=logging.INFO)
asyncio.get_event_loop().run_until_complete(keep_running(bot, cfg.token))
