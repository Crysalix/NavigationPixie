#!/usr/bin/env python3.5
import asyncio
import json
import time
import discord
import traceback

from discord.ext import commands
from pixie_function import *

import config as cfg

class Core:

    def __init__(self, bot):
        self.bot = bot

    def __unload(self):
        pass

    @commands.command(pass_context=True)
    async def checkmodule(self, ctx, arg1):
        if ctx.message.author.id == cfg.bot_ownerid:
            if arg1:
                res = checkModule(arg1)
                if res.returncode == 0:
                    await self.bot.say('OK !')
                else:
                    await self.bot.say('```' + str(res.stderr.decode().strip()) + '```')

    @commands.command(pass_context=True)
    async def checkconfig(self, ctx, *args):
        if ctx.message.author.id == ctx.message.author.server.owner.id:
            if args:
                for module in args:
                    if validateModuleName(module):
                        if checkModuleConfig(module, ctx.message.author.server.id):
                            await self.bot.say('OK !')
                        else:
                            await self.bot.say('Configuration incomplete !')
                    else:
                        await self.bot.say('Unknown module **' + module + '**.')
            else:
                await self.bot.say('Missing module name !')
                    
    #MODULE LOAD/UNLOAD/RELOAD COMMAND (BOTMASTER ONLY)
    @commands.command(pass_context=True)
    async def load(self, ctx, *args):
        """Load custom bot modules."""
        if ctx.message.author.id == cfg.bot_ownerid:
            if args:
                listmodules = readData('main')
                for module in args:
                    try:
                        if module == 'core':
                            await self.bot.say('Did you mean `!reload core` ? <:derp:443087292605923339>')
                        elif listmodules[module]["last"] == "loaded":
                            await self.bot.say('Module **' + module + '** already loaded.')
                        else:
                            res = checkModule(module)
                            if res.returncode != 0:
                                await self.bot.say('```' + str(res.stderr.decode().strip()) + '```')
                            else:
                                try:
                                    self.bot.load_extension('module_' + module)
                                except ImportError:
                                    await self.bot.say('Failed to load module **' + module + '**.')
                                except SyntaxError:
                                    await self.bot.say('Bad module **' + module + '**.')
                                except NameError:
                                    await self.bot.say('```' + traceback.format_exc() + '```')
                                    self.bot.unload_extension('module_' + module)
                                except discord.ClientException:
                                    await self.bot.say('```' + traceback.format_exc() + '```')
                                else:
                                    listmodules[module]["last"] = "loaded"
                                    await self.bot.say('Done !')
                    except KeyError:
                        await self.bot.say('Unknown module **' + module + '**.')
                saveData('main', listmodules)
            else:
                await self.bot.say('Missing module name !')

    @commands.command(pass_context=True)
    async def unload(self, ctx, *args):
        """Unload custom bot modules."""
        if ctx.message.author.id == cfg.bot_ownerid:
            if args:
                listmodules = readData('main')
                for module in args:
                    try:
                        if module == 'core':
                            await self.bot.say('I can\'t unload core module ! You fool !')
                        elif listmodules[module]["last"] == "unloaded":
                            await self.bot.say('Module **' + module + '** already unloaded.')
                        else:
                            self.bot.unload_extension('module_' + module)
                            listmodules[module]["last"] = "unloaded"
                            await self.bot.say('Done !')
                    except KeyError:
                        await self.bot.say('Unknown module **' + module + '**.')
                saveData('main', listmodules)
            else:
                await self.bot.say('Missing module name !')

    @commands.command(pass_context=True)
    async def reload(self, ctx, *args):#IMPROVE, KEYERROR NOT RAISED !
        """Reload given bot modules, or all modules."""
        if ctx.message.author.id == cfg.bot_ownerid:
            listmodules = readData('main')
            if args:
                for module in args:
                    try:
                        res = checkModule(module)
                        if res.returncode != 0:
                            await self.bot.say('```py\n' + str(res.stderr.decode().strip()) + '```')
                        elif (module == "core" or listmodules[module]["last"] == "loaded"):
                            self.bot.unload_extension('module_' + module)
                            try:
                                self.bot.load_extension('module_' + module)
                            except ImportError:
                                if module != "core":
                                    listmodules[module]["last"] = "unloaded"
                                await self.bot.say('Failed to reload module **' + module + '**.')
                                break
                            except SyntaxError:
                                if module != "core":
                                    listmodules[module]["last"] = "unloaded"
                                await self.bot.say('Bad module **' + module + '**.')
                                break
                            await self.bot.say('Done !')
                    except KeyError:
                        await self.bot.say('Unknown module **' + module + '**.')
            else:
                for module in listmodules:
                    if listmodules[module]["last"] == "loaded":
                        self.bot.unload_extension('module_' + module)
                        try:
                            self.bot.load_extension('module_' + module)
                        except ImportError:
                            if module != "core":
                                listmodules[module]["last"] = "unloaded"
                            await self.bot.say('Failed to reload module **' + module + '**.')
                        except SyntaxError:
                            if module != "core":
                                listmodules[module]["last"] = "unloaded"
                            await self.bot.say('Bad module **' + module + '**.')
                await self.bot.say('Done !')
            saveData('main', listmodules)

    #MODULE ENABLE/DISABLE COMMAND (SERVERADMIN ONLY)
    @commands.command(pass_context=True)
    async def enable(self, ctx, *args):
        if ctx.message.author.id == ctx.message.author.server.owner.id:
            if args:
                listmodules = readData('main')
                for module in args:
                    try:
                        if module == "core":
                            raise KeyError
                        serverlistmodules = readData('server', ctx.message.author.server.id, module)
                        listmodules[module]
                    except KeyError:
                        await self.bot.say('Unknown module **' + module + '**.')
                    else:
                        if serverlistmodules[module]["last"] == "enabled":
                            await self.bot.say('Module **' + module + '** already enabled.')
                        elif checkModuleConfig(module, ctx.message.author.server.id):
                            serverlistmodules[module]["last"] = "enabled"
                            saveData('server', serverlistmodules, ctx.message.author.server.id)
                            await self.bot.say('Done !')
                        else:
                            await self.bot.say('Module **' + module + '** is not configured.')
            else:
                await self.bot.say('Missing module name !')

    @commands.command(pass_context=True)
    async def disable(self, ctx, *args):
        if ctx.message.author.id == ctx.message.author.server.owner.id:
            if args:
                listmodules = readData('main')
                for module in args:
                    try:
                        if module == "core":
                            raise KeyError
                        serverlistmodules = readData('server', ctx.message.author.server.id)
                        listmodules[module]
                    except KeyError:
                        await self.bot.say('Unknown module **' + module + '**.')
                    else:
                        if serverlistmodules[module]["last"] == "disabled":
                            await self.bot.say('Module **' + module + '** already disabled.')
                        else:
                            serverlistmodules[module]["last"] = "disabled"
                            saveData('server', serverlistmodules, ctx.message.author.server.id)
                            await self.bot.say('Done !')
            else:
                await self.bot.say('Missing module name !')

    #MODULE LIST VIEWER
    @commands.command(pass_context=True)
    async def module(self, ctx):
        """Module list generator"""
        if(ctx.message.author.id == cfg.bot_ownerid or ctx.message.author.id == ctx.message.author.server.owner.id):
            listmodules = readData('main')
            serverlistmodules = readData('server', ctx.message.author.server.id)
            if ctx.message.author.id == cfg.bot_ownerid:
                embed = discord.Embed(description=':gear: Module list :', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                for module in listmodules:
                    if module != 'core':
                        try:
                            serverlistmodules[module]["last"]
                        except KeyError:
                            serverlistmodules[module] = getDefault(module)
                        embed.add_field(name='**Module ' + module + '**\nmodule_' + module + '.py', value='**Default : ' + listmodules[module]["default"] + '**\nActual : ' + listmodules[module]["last"] + '\n**Default : ' + serverlistmodules[module]["default"] + '**\nActual : ' + serverlistmodules[module]["last"], inline=True)
                await self.bot.send_message(ctx.message.channel, embed=embed)
            if ctx.message.author.id == ctx.message.author.server.owner.id:
                embed = discord.Embed(description=':gear: Module list :', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                legend = ':white_check_mark:>Enabled :x:>Disabled :no_entry:>Unavailable'
                status = ''
                for module in serverlistmodules:
                    if module != "bot":
                        if listmodules[module]["last"] == 'unloaded':
                            status = status + ':no_entry: **' + module + '**\n'
                        elif serverlistmodules[module]["last"] == 'enabled':
                            status = status + ':white_check_mark: **' + module + '**\n'
                        else:
                            status = status + ':x: **' + module + '**\n'
                embed.add_field(name=legend, value=status, inline=False)
                await self.bot.send_message(ctx.message.channel, embed=embed)
    
    #MODULE CONFIGURATION COMMAND
    @commands.command(pass_context=True)
    async def config(self, ctx, *args):
        """Bot module configuration"""
        if ctx.message.author.id == ctx.message.author.server.owner.id:
            if args:
                #module ? or bot config ?
                if (validateModuleName(args[0]) or args[0] == "bot"):
                    serverlistmodule = readData('server', ctx.message.author.server.id)
                    lang = serverlistmodule["bot"]["config"]["lang"]["value"]
                    defaultlistmodule = getDefault()
                    #is configurable ?
                    if defaultlistmodule[args[0]]['config'] == "None":
                        await self.bot.say('This module don\'t need configuration.')
                        return
                    try:
                        args[1]
                    except:#no config key specified
                        if args[0] == 'bot':
                            embed = discord.Embed(title=':gear: Module **' + args[0] + '** configuration :', description='', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                        else:
                            embed = discord.Embed(title=':gear: Module **' + args[0] + '** configuration :', description='(Module is `' + serverlistmodule[args[0]]["last"] + '`)', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                        for cfgkey in serverlistmodule[args[0]]["config"]:
                            embed.add_field(name='**' + cfgkey + '**', value='**Desription** : ' + serverlistmodule[args[0]]["config"][cfgkey]["description"][lang] + '\n**Value** (' + serverlistmodule[args[0]]["config"][cfgkey]["type"] + '): ' + serverlistmodule[args[0]]["config"][cfgkey]["value"], inline=False)
                        embed.set_footer(text='Usage : !config ' + args[0] + ' <ConfigName> <add/remove/set> <value>')
                        await self.bot.send_message(ctx.message.channel, embed=embed)
                        return
                    if validateConfigKey(ctx.message.author.server.id, args[0], args[1]):
                        #configkey ?
                        try:
                            args[2]
                        except:#no value for configkey
                            embed = discord.Embed(title=':gear: Module **' + args[0] + '** configuration :', description='Actual configuration.', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                            embed.add_field(name='**' + args[1] + '**', value='**Desription** : ' + serverlistmodule[args[0]]["config"][args[1]]["description"][lang] + '\n**Value** (' + serverlistmodule[args[0]]["config"][args[1]]["type"] + '): ' + serverlistmodule[args[0]]["config"][args[1]]["value"], inline=False)
                            if serverlistmodule[args[0]]["config"][args[1]]["type"] == 'bool':
                                embed.set_footer(text='Usage : !config ' + args[0] + args[1] + ' <ConfigName> <set> <true/false>')
                            else:
                                embed.set_footer(text='Usage : !config ' + args[0] + args[1] + ' <ConfigName> <set/add/remove> <value>')
                            await self.bot.send_message(ctx.message.channel, embed=embed)
                            return
                        if(args[2] == 'remove' or args[2] == 'clear'):
                            if args[2] == 'remove':
                                try:
                                    args[3]
                                except IndexError:
                                    await self.bot.say('DEBUG : Remove action need a value!')
                                else:
                                    await self.bot.say('Command not yet supported')
                                    return
                                    removeConfig('remove', ctx.message.author.server.id, args[0], args[1], args[3])
                            elif args[2] == 'clear':
                                try:
                                    args[3]
                                except IndexError:
                                    removeConfig('clear', ctx.message.author.server.id, args[0], args[1])
                                else:
                                    await self.bot.say('clear option don\t need arguments.')
                        elif(args[2] == 'add' or args[2] == 'set'):
                            try:
                                args[3]
                            except IndexError:
                                await self.bot.say('DEBUG : Missing value !')
                            else:
                                if validateConfigKeyType(ctx.message.author.server.id, serverlistmodule[args[0]]["config"][args[1]]["type"], args[0], args[1], args[3]):
                                    #configkey valid ?
                                    serverlistmodule[args[0]]["config"][args[1]]["value"] = args[3]
                                    saveData('server', serverlistmodule, ctx.message.author.server.id)
                                    embed = discord.Embed(title=':gear: Module **' + args[0] + '** configuration :', description='New configuration saved !', colour=0x00FF00, timestamp=datetime.datetime.utcnow())
                                    embed.add_field(name='**' + args[1] + '**', value='**Desription** : ' + serverlistmodule[args[0]]["config"][args[1]]["description"][lang] + '\n**Value** (' + serverlistmodule[args[0]]["config"][args[1]]["type"] + '): ' + serverlistmodule[args[0]]["config"][args[1]]["value"], inline=False)
                                    await self.bot.send_message(ctx.message.channel, embed=embed)
                                else:#bad value
                                    await self.bot.say('DEBUG : Wrong value !')
                        else:
                            await self.bot.say('DEBUG : ACTION NEEDED !')
                    else:#bad config key
                        await self.bot.say('DEBUG : Bad config key !')
                else:#module unknown
                    await self.bot.say('Unknown module **' + args[0] + '**.')
            else:#module missing
                embed = discord.Embed(description=':gear: Module configuration :', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                embed.add_field(name='Usage :', value='!config <module> <configkey> <add/remove/set/clear> <value>', inline=False)
                embed.add_field(name='Example :', value='!config welcome message set "Hello and welcome to my awesome server !"', inline=False)
                await self.bot.send_message(ctx.message.channel, embed=embed)

def setup(bot):
    bot.add_cog(Core(bot))
