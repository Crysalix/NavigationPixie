#!/usr/bin/env python3
import aiohttp
import asyncio
import datetime
import discord
import logging
import subprocess
import time
import traceback
import websockets
import sys

from discord.ext import commands
from discord.utils import get
from pixie_function import *

import config as cfg
# import backoff

listmodules = readData('main')

bot = commands.Bot(command_prefix='!', description='Navigation Pixie')
bot.remove_command('help')

# async def keep_running(client, token):
    # retry = backoff.ExponentialBackoff()
    # while True:
        # try:
            # await client.login(token)
        # except (discord.HTTPException, aiohttp.ClientError):
            # logging.exception("Discord.py pls login")
            # await asyncio.sleep(retry.delay())
        # else:
            # break
    # while client.is_logged_in:
        # if client.is_closed:
            # client._closed.clear()
            # client.http.recreate()
        # try:
            # await client.connect()
        # except (discord.HTTPException, aiohttp.ClientError,
                # discord.GatewayNotFound, discord.ConnectionClosed,
                # websockets.InvalidHandshake,
                # websockets.WebSocketProtocolError) as e:
            # if isinstance(e, discord.ConnectionClosed) and e.code == 4004:
                # raise # Do not reconnect on authentication failure
            # logging.exception("Discord.py pls keep running")
            # await asyncio.sleep(retry.delay())

@bot.event
async def on_ready():
    chan = bot.get_channel(cfg.botlog_chan)
    logging.info('NAVIGATIONPIXIE > Logged in as {} with ID {}'.format(bot.user.name, bot.user.id))
    await chan.send('Connected ! Loading modules...')
    #Loading core module first
    try:
        bot.load_extension('modules.core')
    except ImportError:
        await chan.send('<@{}> Failed to load core module ! Can\'t init bot instance !'.format(cfg.bot_ownerid))
        logging.error('NAVIGATIONPIXIE > Failed to load core module ! Can\'t init bot instance !')
        await bot.close()
        sys.exit()
    except SyntaxError:
        if module == 'core':
            await chan.send('<@{}> Syntax error on core module ! Can\'t init bot instance !'.format(cfg.bot_ownerid))
            logging.error('NAVIGATIONPIXIE > Syntax error on core module ! Can\'t init bot instance !')
            await bot.close()
            sys.exit()
    #Loading modules
    for module in listmodules:
        if (listmodules[module]["default"] == "loaded" or listmodules[module]["default"] == "global"):
            try:
                bot.load_extension('modules.' + module)
            except ImportError:
                await chan.send('```py\n%s\n```' % traceback.format_exc())
                logging.error('NAVIGATIONPIXIE > Failed to load module {}.'.format(module))
            except SyntaxError:
                await chan.send('```py\n%s\n```' % traceback.format_exc())
                logging.warning('NAVIGATIONPIXIE > Bad module : {}'.format(module))
    await chan.send('Ready !')
    logging.info('NAVIGATIONPIXIE > Connected !')

@bot.event
async def on_resumed():
   logging.warning('NAVIGATIONPIXIE > Session resumed...')

# @bot.event
# async def on_command():

@bot.event
async def on_command_error(ctx, error):
    if not str(error) == 'Command "' + ctx.invoked_with + '" is not found':
        await bot.get_channel(cfg.botlog_chan).send('<@{}>'.format(cfg.bot_ownerid))
        embed = discord.Embed(title=':x: Command Error', colour=0x992d22, timestamp=datetime.datetime.utcnow())
        embed.description = '```py\n%s\n```' % traceback.format_exc()
        embed.add_field(name='Error', value=error)
        embed.add_field(name='Server', value=ctx.message.guild.name)
        embed.add_field(name='Channel', value='<#{}>'.format(ctx.message.channel.id))
        embed.add_field(name='User', value='<@{}>'.format(ctx.message.author.id))
        embed.add_field(name='Command', value='`{}`'.format(ctx.message.clean_content))
        embed.set_footer(text='on_command_error')
        await bot.get_channel(cfg.botlog_chan).send(embed=embed)

@bot.event
async def on_error(event, *args, **kwargs):
    await bot.get_channel(cfg.botlog_chan).send('<@{}>'.format(cfg.bot_ownerid))
    embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c, timestamp=datetime.datetime.utcnow())
    embed.description = '```py\n%s\n```' % traceback.format_exc()
    embed.add_field(name='Event', value=event)
    embed.set_footer(text='on_error')
    await bot.get_channel(cfg.botlog_chan).send(embed=embed)

#MISC
@bot.command(pass_context=True)
async def restart(ctx):
    if ctx.message.author.id == cfg.bot_ownerid:
        chan = ctx.message.channel
        logging.info('NAVIGATIONPIXIE > Restart')
        await chan.send('I`ll be back !')
        await bot.close()

@bot.command(pass_context=True)
async def quit(ctx):
    if ctx.message.author.id == cfg.bot_ownerid:
        chan = ctx.message.channel
        logging.info('NAVIGATIONPIXIE > SystemExit')
        await chan.send('Goodbye !')
        await bot.close()
        sys.exit()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        #logging commands only (including unknown commands)
        logging.info('{0.guild.name} > {0.content}'.format(message))
    if bot.user.mentioned_in(message):
        try:
            emoji = bot.get_emoji(443086928716496897)
            await message.add_reaction(emoji)
        except:
            await bot.get_channel(cfg.botlog_chan).send('```py\n%s\n```' % traceback.format_exc())
    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    em = discord.Embed(title=guild.name, type='rich', description='Total : {}'.format(str(len(bot.servers))), colour=0x23d160, timestamp=datetime.datetime.utcnow())
    em.set_author(name='New server joined !', icon_url=guild.icon_url)
    em.set_thumbnail(url=guild.icon_url)
    em.add_field(name='ID', value=guild.id)
    em.add_field(name='Region', value=guild.region)
    em.add_field(name='Owner', value='<@{}>'.format(guild.owner.id))
    em.add_field(name='Members', value=guild.member_count)
    em.add_field(name='Created at', value=guild.created_at)
    roles = ''
    for e in guild.role_hierarchy:
        roles = roles + e.name + ' '
    em.add_field(name='Roles', value=roles)
    em.add_field(name='2FA', value=guild.mfa_level)
    await bot.get_channel(cfg.botlog_chan).send(embed=em)

@bot.event
async def on_guild_remove(guild):
    em = discord.Embed(title=guild.name, type='rich', description='Total : {}'.format(str(len(bot.servers))), colour=0xe74c3c, timestamp=datetime.datetime.utcnow())
    em.set_author(name='Server removed !', icon_url=guild.icon_url)
    em.set_thumbnail(url=guild.icon_url)
    em.add_field(name='ID', value=guild.id)
    em.add_field(name='Region', value=guild.region)
    em.add_field(name='Owner', value='<@{}>'.format(guild.owner.id))
    em.add_field(name='Members', value=guild.member_count)
    em.add_field(name='Created at', value=guild.created_at)
    em.add_field(name='2FA', value=guild.mfa_level)
    await bot.get_channel(cfg.botlog_chan).send(embed=em)

logging.basicConfig(format='%(asctime)s | [%(levelname)s] | %(message)s', datefmt='%m/%d/%Y - %H:%M:%S', filename='latest.log',level=logging.INFO)
bot.run(cfg.token)
# asyncio.get_event_loop().run_until_complete(keep_running(bot, cfg.token))
