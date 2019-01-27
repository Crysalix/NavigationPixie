#!/usr/bin/env python3
import asyncio
import datetime
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

    @commands.command(name='import')
    @commands.is_owner()
    async def _import(self, ctx, arg1 = None):
        """Import new module then add new data/config."""
        if arg1:
            try:
                self.bot.load_extension('modules.' + arg1)
                listmodules = readData('main')
                listmodules.update({arg1: {"last": "unloaded", "default": "unloaded"}})
                saveData('main', listmodules)
                default = getDefault()
                if default[arg1]:
                    await ctx.send('Done !')
            except ImportError:
                await ctx.send('Module not found !')
            except discord.ClientException:
                await ctx.send('Can\'t import module, setup function is missing.')
            except KeyError:
                await ctx.send('Done. Added default config value !')
                default.update({arg1: {"config": "None", "default": "disabled", "last": "disabled"}})
                saveData('default', default)
            except:
                await ctx.send('```py\n%s\n```' % traceback.format_exc())
        else:
            await ctx.send('Module name required !')

    @commands.command()
    @commands.is_owner()
    async def remove(self, ctx, arg1 = None):
        """Remove a module and configs value."""
        if arg1:
            try:
                self.bot.unload_extension('modules.' + arg1)
                listmodules = readData('main')
                del listmodules[arg1]
                saveData('main', listmodules)
                default = getDefault()
                del default[arg1]
                saveData('default', default)
                await ctx.send('Done !')
            except ImportError:
                await ctx.send('ImportError')
            except discord.ClientException:
                await ctx.send('discord.ClientException')
            except KeyError:
                await ctx.send('KeyError')
            except:
                await ctx.send('```py\n%s\n```' % traceback.format_exc())
        else:
            await ctx.send('Module name required !')

    @commands.command()
    @commands.is_owner()
    async def checkmodule(self, ctx, arg1):
        if arg1:
            res = checkModule(arg1)
            if res.returncode == 0:
                await ctx.send('OK !')
            else:
                await ctx.send('```py\n' + str(res.stderr.decode().strip()) + '```')
        else:
            await ctx.send('Module name required !')

    #MODULE LOAD/UNLOAD/RELOAD COMMAND (BOTMASTER ONLY)
    @commands.command()
    async def load(self, ctx, *args):
        """Load custom bot modules."""
        if ctx.message.author.id == cfg.bot_ownerid:
            chan = ctx.message.channel
            if args:
                listmodules = readData('main')
                for module in args:
                    try:
                        if module == 'core':
                            await chan.send('Did you mean `!reload core` ? <:derp:443087292605923339>')
                        elif listmodules[module]["last"] == "loaded":
                            await chan.send('Module **{}** already loaded.'.format(module))
                        else:
                            res = checkModule(module)
                            if res.returncode != 0:
                                await chan.send('```py\n' + str(res.stderr.decode().strip()) + '```')
                            else:
                                try:
                                    self.bot.load_extension('modules.' + module)
                                except ImportError:
                                    await chan.send('Failed to load module **{}**.'.format(module))
                                except:
                                    await chan.send('```py\n%s\n```' % traceback.format_exc())
                                else:
                                    listmodules[module]["last"] = "loaded"
                                    await chan.send('Done !')
                    except KeyError:
                        await chan.send('Unknown module **{}**.'.format(module))
                saveData('main', listmodules)
            else:
                await chan.send('Missing module name !')

    @commands.command()
    async def unload(self, ctx, *args):
        """Unload custom bot modules."""
        if ctx.message.author.id == cfg.bot_ownerid:
            chan = ctx.message.channel
            if args:
                listmodules = readData('main')
                for module in args:
                    try:
                        if module == 'core':
                            await chan.send('I can\'t unload core module ! You fool !')
                        elif listmodules[module]["last"] == "unloaded":
                            await chan.send('Module **{}** already unloaded.'.format(module))
                        else:
                            self.bot.unload_extension('modules.' + module)
                            listmodules[module]["last"] = "unloaded"
                            await chan.send('Done !')
                    except KeyError:
                        await chan.send('Unknown module **{}**.'.format(module))
                saveData('main', listmodules)
            else:
                await chan.send('Missing module name !')

    @commands.command()
    async def reload(self, ctx, *args):#IMPROVE, KEYERROR NOT RAISED !
        """Reload given bot modules, or all modules."""
        if ctx.message.author.id == cfg.bot_ownerid:
            listmodules = readData('main')
            chan = ctx.message.channel
            if args:
                for module in args:
                    try:
                        res = checkModule(module)
                        if res.returncode != 0:
                            await chan.send('```py\n' + str(res.stderr.decode().strip()) + '```')
                        elif (module == "core" or listmodules[module]["last"] == "loaded"):
                            self.bot.unload_extension('modules.' + module)
                            try:
                                self.bot.load_extension('modules.' + module)
                            except ImportError:
                                if module != "core":
                                    listmodules[module]["last"] = "unloaded"
                                await chan.send('Failed to reload module **{}**.'.format(module))
                                break
                            except SyntaxError:
                                if module != "core":
                                    listmodules[module]["last"] = "unloaded"
                                await chan.send('Bad module **{}**.'.format(module))
                                break
                            await chan.send('Done !')
                        else:
                            await chan.send('Module {0} is not loaded.'.format(module))
                            #await chan.send(self.locales[lang]['core']['messages']['notloaded'].format(module))
                    except KeyError:
                        await chan.send('Unknown module **{}**.'.format(module))
            else:
                for module in listmodules:
                    if listmodules[module]["last"] == "loaded":
                        self.bot.unload_extension('modules.' + module)
                        try:
                            self.bot.load_extension('modules.' + module)
                        except ImportError:
                            if module != "core":
                                listmodules[module]["last"] = "unloaded"
                            await chan.send('Failed to reload module **{}**.'.format(module))
                        except SyntaxError:
                            if module != "core":
                                listmodules[module]["last"] = "unloaded"
                            await chan.send('Bad module **{}**.'.format(module))
                await chan.send('Done !')
            saveData('main', listmodules)

    #MODULE ENABLE/DISABLE COMMAND (SERVERADMIN ONLY)
    @commands.command()
    async def enable(self, ctx, *args):
        if ctx.message.author.id == ctx.message.author.guild.owner.id:
            serverlistmodules = readData('server', ctx.message.author.guild.id)
            lang = serverlistmodules['bot']['config']['lang']['value']
            chan = ctx.message.channel
            if args:
                listmodules = readData('main')
                for module in args:
                    try:
                        if module == "core":
                            raise KeyError
                        serverlistmodules = readData('server', ctx.message.author.guild.id, module)
                        listmodules[module]
                    except KeyError:
                        await chan.send(self.locales[lang]['core']['messages']['nomodule'].format(module))
                    else:
                        if serverlistmodules[module]["default"] == "global":
                            await chan.send(self.locales[lang]['core']['messages']['noenabledisable'])
                        elif serverlistmodules[module]["last"] == "enabled":
                            await chan.send(self.locales[lang]['core']['messages']['alreadyenabled'].format(module))
                        elif checkModuleConfig(module, ctx.message.author.guild.id):
                            serverlistmodules[module]["last"] = "enabled"
                            saveData('server', serverlistmodules, ctx.message.author.guild.id)
                            await chan.send('Done !')
                        else:
                            await chan.send(self.locales[lang]['core']['messages']['noconfig'])
            else:
                await chan.send(self.locales[lang]['core']['messages']['modulerequired'])

    @commands.command()
    async def disable(self, ctx, *args):
        if ctx.message.author.id == ctx.message.author.guild.owner.id:
            serverlistmodules = readData('server', ctx.message.author.guild.id)
            lang = serverlistmodules['bot']['config']['lang']['value']
            chan = ctx.message.channel
            if args:
                listmodules = readData('main')
                for module in args:
                    try:
                        if module == "core":
                            raise KeyError
                        serverlistmodules = readData('server', ctx.message.author.guild.id)
                        listmodules[module]
                    except KeyError:
                        await chan.send(self.locales[lang]['core']['messages']['nomodule'].format(module))
                    else:
                        if serverlistmodules[module]["default"] == "global":
                            await chan.send(self.locales[lang]['core']['messages']['noenabledisable'])
                        elif serverlistmodules[module]["last"] == "disabled":
                            await chan.send(self.locales[lang]['core']['messages']['alreadydisabled'].format(module))
                        else:
                            serverlistmodules[module]["last"] = "disabled"
                            saveData('server', serverlistmodules, ctx.message.author.guild.id)
                            await chan.send('Done !')
            else:
                await chan.send(self.locales[lang]['core']['messages']['modulerequired'])

    #MODULE LIST VIEWER
    @commands.command()
    async def module(self, ctx):
        """Module list generator"""
        if(ctx.message.author.id == cfg.bot_ownerid or ctx.message.author.id == ctx.message.author.guild.owner.id):
            listmodules = readData('main')
            serverlistmodules = readData('server', ctx.message.author.guild.id)
            chan = ctx.message.channel
            if ctx.message.author.id == cfg.bot_ownerid and ctx.message.channel.id == cfg.botlog_chan:
                embed = discord.Embed(description=':gear: Module list :', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                for module in sorted(listmodules):
                    if module != 'core':
                        try:
                            serverlistmodules[module]["last"]
                        except KeyError:
                            serverlistmodules[module] = getDefault(module)
                        embed.add_field(name='**Module ' + module + '**\nmodule_' + module + '.py', value='**Default : ' + listmodules[module]["default"] + '**\nActual : ' + listmodules[module]["last"] + '\n**Default : ' + serverlistmodules[module]["default"] + '**\nActual : ' + serverlistmodules[module]["last"], inline=True)
                await chan.send(embed=embed)
            if ctx.message.author.id == ctx.message.author.guild.owner.id:
                embed = discord.Embed(description=':gear: Module list :', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                legend = ':white_check_mark:>Enabled :x:>Disabled :no_entry:>Unavailable :globe_with_meridians:>Global'
                for module in sorted(serverlistmodules):
                    if module != "bot":
                        try:
                            if listmodules[module]["last"] == 'unloaded':
                                embed.add_field(name='Module {}'.format(module), value='> :no_entry:', inline=True)
                            elif serverlistmodules[module]["last"] == 'global':
                                embed.add_field(name='Module {}'.format(module), value='> :globe_with_meridians:', inline=True)
                            elif serverlistmodules[module]["last"] == 'enabled':
                                embed.add_field(name='Module {}'.format(module), value='> :white_check_mark:', inline=True)
                            else:
                                embed.add_field(name='Module {}'.format(module), value='> :x:', inline=True)
                        except KeyError:#when data is found for removed module.
                            pass
                embed.add_field(name='Legend :', value=legend, inline=False)
                await chan.send(embed=embed)
    
    #MODULE CONFIGURATION COMMAND
    @commands.command()
    async def config(self, ctx, *args):
        """Bot module configuration"""
        if ctx.message.author.id == ctx.message.author.guild.owner.id:
            chan = ctx.message.channel
            if args:
                serverlistmodule = readData('server', ctx.message.author.guild.id)
                lang = serverlistmodule["bot"]["config"]["lang"]["value"]
                #module ? or bot config ?
                module = args[0]
                if (validateModuleName(module) or module == "bot"):
                    defaultlistmodule = getDefault()
                    #is configurable ?
                    if defaultlistmodule[module]['config'] == "None":
                        await chan.send(self.locales[lang]['core']['messages']['noconfigneeded'])
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
                        await chan.send(embed=embed)
                        return
                    if validateConfigKey(ctx.message.author.guild.id, module, configKey):
                        #configkey action ?
                        try:
                            action = args[2]
                        except:#no action specified
                            embed = discord.Embed(title=':gear: Module **' + module + '** configuration :', description=self.locales[lang]['core']['messages']['actualconf'], colour=0x7289da, timestamp=datetime.datetime.utcnow())
                            embed.add_field(name='**' + configKey + '**', value='**Description** : ' + self.locales[lang][module]['config'][configKey] + '\n**Value** (' + serverlistmodule[module]["config"][configKey]["type"] + '): ' + serverlistmodule[module]["config"][configKey]["value"], inline=False)
                            validAction = getValidAction(module, configKey)
                            embed.set_footer(text='Usage : !config ' + module + ' ' + configKey + ' ' + validAction + ' (value)')
                            await chan.send(embed=embed)
                            return
                        if(action == 'remove' or action == 'clear'):
                            if action == 'remove':
                                #canRemove ?
                                if (serverlistmodule[module]["config"][configKey]["type"] == 'chantaglist' or serverlistmodule[module]["config"][configKey]["type"] == 'usertaglist'):
                                    try:
                                        args[3]
                                    except IndexError:
                                        await chan.send(self.locales[lang]['core']['messages']['actionargmissing'] + '\n`!config <module> <configKey> <remove> <value>`')
                                    else:
                                        await chan.send('Command not yet supported')
                                        return
                                        removeConfig('remove', ctx.message.author.guild.id, module, configKey, args[3])
                                else:
                                    await chan.send(self.locales[lang]['core']['messages']['cantuseaction'].format(action, configKey, 'clear'))
                            elif action == 'clear':
                                try:
                                    args[3]
                                except IndexError:
                                    removeConfig('clear', ctx.message.author.guild.id, module, configKey)
                                    if checkModuleConfig(module, ctx.message.author.guild.id):
                                        await chan.send(self.locales[lang]['core']['messages']['configclear'])
                                    else:
                                        serverlistmodule[module]["last"] = "disabled"
                                        saveData('server', serverlistmodule, ctx.message.author.guild.id)
                                        await chan.send(self.locales[lang]['core']['messages']['configclear'] + self.locales[lang]['core']['messages']['needreconfig'])
                                else:
                                    await chan.send(self.locales[lang]['core']['messages']['clearnoarg'])
                        elif(action == 'add' or action == 'set'):
                            if action == 'add':
                                if (serverlistmodule[module]["config"][configKey]["type"] == 'chantaglist' or serverlistmodule[module]["config"][configKey]["type"] == 'usertaglist'):
                                    try:
                                        args[3]
                                    except IndexError:
                                        await chan.send(self.locales[lang]['core']['messages']['actionargmissing'] + '\n`!config <module> <configKey> <add> <value>`')
                                    else:
                                        if validateConfigKeyType(ctx.message.author.guild.id, serverlistmodule[module]["config"][configKey]["type"], module, configKey, args[3]):
                                            await chan.send('Command not yet supported')
                                            return
                                        else:#bad value
                                            await chan.send(self.locales[lang]['core']['messages']['invalidvalue'])
                                else:
                                    await chan.send(self.locales[lang]['core']['messages']['cantuseaction'].format(action, configKey, 'set'))
                            elif action == 'set':
                                try:
                                    args[3]
                                except IndexError:
                                    await chan.send(self.locales[lang]['core']['messages']['actionargmissing'] + '\n`!config <module> <configKey> <set> <value>`')
                                else:
                                    if validateConfigKeyType(ctx.message.author.guild.id, serverlistmodule[module]["config"][configKey]["type"], module, configKey, args[3]):
                                        if validateValue(module, configKey, args[3]):
                                            serverlistmodule[module]["config"][configKey]["value"] = args[3]
                                            saveData('server', serverlistmodule, ctx.message.author.guild.id)
                                            embed = discord.Embed(title=':gear: Module **' + module + '** configuration :', description=self.locales[lang]['core']['messages']['configsaved'], colour=0x00FF00, timestamp=datetime.datetime.utcnow())
                                            embed.add_field(name='**' + configKey + '**', value='**Description** : ' + self.locales[lang][module]['config'][configKey] + '\n**Value** (' + serverlistmodule[module]["config"][configKey]["type"] + '): ' + serverlistmodule[module]["config"][configKey]["value"], inline=False)
                                            await chan.send(embed=embed)
                                        else:
                                            await chan.send(self.locales[lang]['core']['messages']['invalidvalue'])
                                    else:#bad value
                                        await chan.send(self.locales[lang]['core']['messages']['invalidvalue'])
                        else:
                            validAction = getValidAction(module, configKey)
                            await chan.send('Valid action for `' + configKey + '` is `' + validAction + '`')
                    else:#bad config key
                        await chan.send(self.locales[lang]['core']['messages']['badconfigkey'])
                else:#module unknown
                    await chan.send(self.locales[lang]['core']['messages']['nomodule'].format(module))
            else:#module missing
                embed = discord.Embed(description=':gear: Module configuration :', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                embed.add_field(name='Usage :', value='!config <module> <configKey> <add/remove/set/clear> (value)', inline=False)
                embed.add_field(name='Example :', value='!config welcome message set "Hello and welcome to my awesome server !"', inline=False)
                await chan.send(embed=embed)

    @commands.command()
    async def checkconfig(self, ctx, *args):
        if ctx.message.author.id == ctx.message.author.guild.owner.id:
            serverlistmodules = readData('server', ctx.message.author.guild.id)
            lang = serverlistmodules['bot']['config']['lang']['value']
            chan = ctx.message.channel
            if args:
                for module in args:
                    if validateModuleName(module):
                        if checkModuleConfig(module, ctx.message.author.guild.id):
                            await chan.send('OK !')
                        else:
                            await chan.send(self.locales[lang]['core']['messages']['noconfig'])
                    else:
                        await chan.send(self.locales[lang]['core']['messages']['nomodule'].format(module))
            else:
                await chan.send(self.locales[lang]['core']['messages']['modulerequired'])

def setup(bot):
    bot.add_cog(Core(bot))
