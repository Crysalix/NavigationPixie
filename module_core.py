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
        self.locales = readData('locales')

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
                    await self.bot.say('```py\n' + str(res.stderr.decode().strip()) + '```')
            else:
                await self.bot.say('Module name required !')

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
                                await self.bot.say('```py' + str(res.stderr.decode().strip()) + '```')
                            else:
                                try:
                                    self.bot.load_extension('module_' + module)
                                except ImportError:
                                    await self.bot.say('Failed to load module **' + module + '**.')
                                except SyntaxError:
                                    await self.bot.say('```py\n%s\n```' % traceback.format_exc())
                                except NameError:
                                    await self.bot.say('```py\n%s\n```' % traceback.format_exc())
                                    self.bot.unload_extension('module_' + module)
                                except discord.ClientException:
                                    await self.bot.say('```py\n%s\n```' % traceback.format_exc())
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
            serverlistmodules = readData('server', ctx.message.author.server.id)
            lang = serverlistmodules['bot']['config']['lang']['value']
            if args:
                listmodules = readData('main')
                for module in args:
                    try:
                        if module == "core":
                            raise KeyError
                        serverlistmodules = readData('server', ctx.message.author.server.id, module)
                        listmodules[module]
                    except KeyError:
                        await self.bot.say(self.locales[lang]['core']['messages']['nomodule'].format(module))
                    else:
                        if serverlistmodules[module]["default"] == "global":
                            await self.bot.say(self.locales[lang]['core']['messages']['noenabledisable'])
                        elif serverlistmodules[module]["last"] == "enabled":
                            await self.bot.say(self.locales[lang]['core']['messages']['alreadyenabled'].format(module))
                        elif checkModuleConfig(module, ctx.message.author.server.id):
                            serverlistmodules[module]["last"] = "enabled"
                            saveData('server', serverlistmodules, ctx.message.author.server.id)
                            await self.bot.say('Done !')
                        else:
                            await self.bot.say(self.locales[lang]['core']['messages']['noconfig'])
            else:
                await self.bot.say(self.locales[lang]['core']['messages']['modulerequired'])

    @commands.command(pass_context=True)
    async def disable(self, ctx, *args):
        if ctx.message.author.id == ctx.message.author.server.owner.id:
            serverlistmodules = readData('server', ctx.message.author.server.id)
            lang = serverlistmodules['bot']['config']['lang']['value']
            if args:
                listmodules = readData('main')
                for module in args:
                    try:
                        if module == "core":
                            raise KeyError
                        serverlistmodules = readData('server', ctx.message.author.server.id)
                        listmodules[module]
                    except KeyError:
                        await self.bot.say(self.locales[lang]['core']['messages']['nomodule'].format(module))
                    else:
                        if serverlistmodules[module]["default"] == "global":
                            await self.bot.say(self.locales[lang]['core']['messages']['noenabledisable'])
                        elif serverlistmodules[module]["last"] == "disabled":
                            await self.bot.say(self.locales[lang]['core']['messages']['alreadydisabled'].format(module))
                        else:
                            serverlistmodules[module]["last"] = "disabled"
                            saveData('server', serverlistmodules, ctx.message.author.server.id)
                            await self.bot.say('Done !')
            else:
                await self.bot.say(self.locales[lang]['core']['messages']['modulerequired'])

    #MODULE LIST VIEWER
    @commands.command(pass_context=True)
    async def module(self, ctx):
        """Module list generator"""
        if(ctx.message.author.id == cfg.bot_ownerid or ctx.message.author.id == ctx.message.author.server.owner.id):
            listmodules = readData('main')
            serverlistmodules = readData('server', ctx.message.author.server.id)
            if ctx.message.author.id == cfg.bot_ownerid and ctx.message.channel.id == cfg.botlog_chan:
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
                legend = 'Legend :\n:white_check_mark:>Enabled :x:>Disabled\n:no_entry:>Unavailable :globe_with_meridians:>Global'
                status = ''
                for module in serverlistmodules:
                    if module != "bot":
                        if listmodules[module]["last"] == 'unloaded':
                            status = status + ':no_entry: **' + module + '**\n'
                        elif serverlistmodules[module]["last"] == 'global':
                            status = status + ':globe_with_meridians: **' + module + '**\n'
                        elif serverlistmodules[module]["last"] == 'enabled':
                            status = status + ':white_check_mark: **' + module + '**\n'
                        else:
                            status = status + ':x: **' + module + '**\n'
                embed.add_field(name=status, value=legend, inline=False)
                await self.bot.send_message(ctx.message.channel, embed=embed)
    
    #MODULE CONFIGURATION COMMAND
    @commands.command(pass_context=True)
    async def config(self, ctx, *args):
        """Bot module configuration"""
        if ctx.message.author.id == ctx.message.author.server.owner.id:
            if args:
                serverlistmodule = readData('server', ctx.message.author.server.id)
                lang = serverlistmodule["bot"]["config"]["lang"]["value"]
                #module ? or bot config ?
                module = args[0]
                if (validateModuleName(module) or module == "bot"):
                    defaultlistmodule = getDefault()
                    #is configurable ?
                    if defaultlistmodule[module]['config'] == "None":
                        await self.bot.say(self.locales[lang]['core']['messages']['noconfigneeded'])
                        return
                    try:
                        configKey = args[1]
                    except:#no config key specified
                        if module == 'bot':
                            embed = discord.Embed(title=':gear: Module **' + module + '** configuration :', description='', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                        else:
                            embed = discord.Embed(title=':gear: Module **' + module + '** configuration :', description='(Module is `' + serverlistmodule[module]["last"] + '`)', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                        for cfgkey in serverlistmodule[module]["config"]:
                            embed.add_field(name='**' + cfgkey + '**', value='**Description** : ' + self.locales[lang][module]['config'][cfgkey] + '\n**Value** (' + serverlistmodule[module]["config"][cfgkey]["type"] + '): ' + serverlistmodule[module]["config"][cfgkey]["value"], inline=False)
                        embed.set_footer(text='Usage : !config ' + module + ' <configKey> <add/set/remove/clear> (value)')
                        await self.bot.send_message(ctx.message.channel, embed=embed)
                        return
                    if validateConfigKey(ctx.message.author.server.id, module, configKey):
                        #configkey action ?
                        try:
                            action = args[2]
                        except:#no action specified
                            embed = discord.Embed(title=':gear: Module **' + module + '** configuration :', description=self.locales[lang]['core']['messages']['actualconf'], colour=0x7289da, timestamp=datetime.datetime.utcnow())
                            embed.add_field(name='**' + configKey + '**', value='**Description** : ' + self.locales[lang][module]['config'][configKey] + '\n**Value** (' + serverlistmodule[module]["config"][configKey]["type"] + '): ' + serverlistmodule[module]["config"][configKey]["value"], inline=False)
                            validAction = getValidAction(module, configKey)
                            embed.set_footer(text='Usage : !config ' + module + ' ' + configKey + ' ' + validAction + ' (value)')
                            await self.bot.send_message(ctx.message.channel, embed=embed)
                            return
                        if(action == 'remove' or action == 'clear'):
                            if action == 'remove':
                                #canRemove ?
                                if (serverlistmodule[module]["config"][configKey]["type"] == 'chantaglist' or serverlistmodule[module]["config"][configKey]["type"] == 'usertaglist'):
                                    try:
                                        args[3]
                                    except IndexError:
                                        await self.bot.say(self.locales[lang]['core']['messages']['actionargmissing'] + '\n`!config <module> <configKey> <remove> <value>`')
                                    else:
                                        await self.bot.say('Command not yet supported')
                                        return
                                        removeConfig('remove', ctx.message.author.server.id, module, configKey, args[3])
                                else:
                                    await self.bot.say(self.locales[lang]['core']['messages']['cantuseaction'].format(action, configKey, 'clear'))
                            elif action == 'clear':
                                try:
                                    args[3]
                                except IndexError:
                                    removeConfig('clear', ctx.message.author.server.id, module, configKey)
                                    if checkModuleConfig(module, ctx.message.author.server.id):
                                        await self.bot.say(self.locales[lang]['core']['messages']['configclear'])
                                    else:
                                        serverlistmodule[module]["last"] = "disabled"
                                        saveData('server', serverlistmodule, ctx.message.author.server.id)
                                        await self.bot.say(self.locales[lang]['core']['messages']['configclear'] + self.locales[lang]['core']['messages']['needreconfig'])
                                else:
                                    await self.bot.say(self.locales[lang]['core']['messages']['clearnoarg'])
                        elif(action == 'add' or action == 'set'):
                            if action == 'add':
                                if (serverlistmodule[module]["config"][configKey]["type"] == 'chantaglist' or serverlistmodule[module]["config"][configKey]["type"] == 'usertaglist'):
                                    try:
                                        args[3]
                                    except IndexError:
                                        await self.bot.say(self.locales[lang]['core']['messages']['actionargmissing'] + '\n`!config <module> <configKey> <add> <value>`')
                                    else:
                                        if validateConfigKeyType(ctx.message.author.server.id, serverlistmodule[module]["config"][configKey]["type"], module, configKey, args[3]):
                                            await self.bot.say('Command not yet supported')
                                            return
                                        else:#bad value
                                            await self.bot.say(self.locales[lang]['core']['messages']['invalidvalue'])
                                else:
                                    await self.bot.say(self.locales[lang]['core']['messages']['cantuseaction'].format(action, configKey, 'set'))
                            elif action == 'set':
                                try:
                                    args[3]
                                except IndexError:
                                    await self.bot.say(self.locales[lang]['core']['messages']['actionargmissing'] + '\n`!config <module> <configKey> <set> <value>`')
                                else:
                                    if validateConfigKeyType(ctx.message.author.server.id, serverlistmodule[module]["config"][configKey]["type"], module, configKey, args[3]):
                                        if validateValue(module, configKey, args[3]):
                                            serverlistmodule[module]["config"][configKey]["value"] = args[3]
                                            saveData('server', serverlistmodule, ctx.message.author.server.id)
                                            embed = discord.Embed(title=':gear: Module **' + module + '** configuration :', description=self.locales[lang]['core']['messages']['configsaved'], colour=0x00FF00, timestamp=datetime.datetime.utcnow())
                                            embed.add_field(name='**' + configKey + '**', value='**Description** : ' + self.locales[lang][module]['config'][configKey] + '\n**Value** (' + serverlistmodule[module]["config"][configKey]["type"] + '): ' + serverlistmodule[module]["config"][configKey]["value"], inline=False)
                                            await self.bot.send_message(ctx.message.channel, embed=embed)
                                        else:
                                            await self.bot.say(self.locales[lang]['core']['messages']['invalidvalue'])
                                    else:#bad value
                                        await self.bot.say(self.locales[lang]['core']['messages']['invalidvalue'])
                        else:
                            validAction = getValidAction(module, configKey)
                            await self.bot.say('Valid action for `' + configKey + '` is `' + validAction + '`')
                    else:#bad config key
                        await self.bot.say(self.locales[lang]['core']['messages']['badconfigkey'])
                else:#module unknown
                    await self.bot.say(self.locales[lang]['core']['messages']['nomodule'].format(module))
            else:#module missing
                embed = discord.Embed(description=':gear: Module configuration :', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                embed.add_field(name='Usage :', value='!config <module> <configKey> <add/remove/set/clear> (value)', inline=False)
                embed.add_field(name='Example :', value='!config welcome message set "Hello and welcome to my awesome server !"', inline=False)
                await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def checkconfig(self, ctx, *args):
        if ctx.message.author.id == ctx.message.author.server.owner.id:
            serverlistmodules = readData('server', ctx.message.author.server.id)
            lang = serverlistmodules['bot']['config']['lang']['value']
            if args:
                for module in args:
                    if validateModuleName(module):
                        if checkModuleConfig(module, ctx.message.author.server.id):
                            await self.bot.say('OK !')
                        else:
                            await self.bot.say(self.locales[lang]['core']['messages']['noconfig'])
                    else:
                        await self.bot.say(self.locales[lang]['core']['messages']['nomodule'].format(module))
            else:
                await self.bot.say(self.locales[lang]['core']['messages']['modulerequired'])

def setup(bot):
    bot.add_cog(Core(bot))
