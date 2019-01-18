#!/usr/bin/env python3.5
import asyncio
import discord
import json
import random
import time

from discord.ext import commands
from pixie_function import *

class Poll:

    def __init__(self, bot):
        self.bot = bot
        self.locales = readData('locales')

    def __unload(self):
        pass

    @commands.command(pass_context=True)
    async def poll(self, ctx, *args):
        """Submiting simple poll in a easy way"""
        if ctx.message.author == self.bot.user:
            return
        if not isEnabled('poll', ctx.message.author.server.id):
            return
        serverlistmodules = readData('server', ctx.message.author.server.id)
        lang = serverlistmodules['bot']['config']['lang']['value']
        if args:
            if len(args) >= 12:
                await self.bot.say(self.locales[lang]['poll']['messages']['toomanyargs'])
                return
            #Build message
            rep = ''
            repcontent = '\n'
            if len(args) > 1:
                if not len(args) > 2:
                    await self.bot.say(self.locales[lang]['poll']['messages']['morethanonechoice'])
                    return
                num = str(len(args))
                num = int(num)
                num -= 1
                repheader = self.locales[lang]['poll']['messages']['pollfrom'].format(str(num), ctx.message.author.id)
                react_num = (
                    ':one:',
                    ':two:',
                    ':three:',
                    ':four:',
                    ':five:',
                    ':six:',
                    ':seven:',
                    ':eight:',
                    ':nine:',
                    ':keycap_ten:',
                )
                #rebuild with reactions
                count = 0
                req = 0
                for arg in args:
                    if req == 0:
                        repcontent = repcontent + ':bar_chart: \"' + arg + '\"\n'
                        req += 1
                    else:
                        repcontent = repcontent + react_num[count] + ' : ' + arg + '\n'
                        count += 1
                rep = repheader + repcontent
                await self.bot.say(rep + '\n\n' + self.locales[lang]['poll']['messages']['votenow'])
            elif len(args) == 1:
                embed = discord.Embed(title='', description='\n:bar_chart: **' + args[0] + '**', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                if serverlistmodules['bot']['config']['lang']['value'] == 'fr':
                    embed.add_field(name=':thumbup: / :thumbdown:', value='**OUI** / **NON**', inline=False)
                else:
                    embed.add_field(name=':thumbup: / :thumbdown:', value='**YES** / **NO**', inline=False)
                    
                await self.bot.send_message(ctx.message.channel, self.locales[lang]['poll']['messages']['littlepollfrom'].format(ctx.message.author.id), embed=embed)
        else:
            if serverlistmodules['bot']['config']['lang']['value'] == 'fr':
                embed = discord.Embed(title='Sondages express', description='Sondages simples ou à choix multiples (maximum 10 choix).', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                embed.add_field(name='Pour une simple question', value='!poll "ma question"', inline=False)
                embed.add_field(name='Pour un sondage à choix multiple', value='!poll "ma question" "choix 1" "choix 2"', inline=False)
                embed.set_footer(text='N\'oubliez pas les doubles guillemets (").')
                await self.bot.send_message(ctx.message.channel, embed=embed)
            else:
                embed = discord.Embed(title='Express polls', description='Simple poll or with multiple choice (max 10 choices).', colour=0x7289da, timestamp=datetime.datetime.utcnow())
                embed.add_field(name='For a simple poll', value='!poll "my question"', inline=False)
                embed.add_field(name='For a multiple choice poll', value='!poll "my question" "choice 1" "choice 2"', inline=False)
                embed.set_footer(text='Don\'t forget the double quotes. (")')
                await self.bot.send_message(ctx.message.channel, embed=embed)

    #reaction add
    async def on_message(self, message):
        if message.author == self.bot.user:
            #1 item
            if (message.content.startswith("Petit sondage proposé") or message.content.startswith("Little poll submited by")):
                await self.bot.add_reaction(message, '\U0001F44D')
                await self.bot.add_reaction(message, '\U0001F44E')
            #2 item and more
            if (message.content.startswith("Sondage à") or message.content.startswith("Poll with")):
                arg = message.content.split(" ")
                if int(arg[2]) >= 2:
                    await self.bot.add_reaction(message, '\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}')
                    await asyncio.sleep(0.5)
                    await self.bot.add_reaction(message, '\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}')
                    await asyncio.sleep(0.5)
                if int(arg[2]) >= 3:
                    await self.bot.add_reaction(message, '\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}')
                    await asyncio.sleep(0.5)
                if int(arg[2]) >= 4:
                    await self.bot.add_reaction(message, '\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}')
                    await asyncio.sleep(0.5)
                if int(arg[2]) >= 5:
                    await self.bot.add_reaction(message, '\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}')
                    await asyncio.sleep(0.5)
                if int(arg[2]) >= 6:
                    await self.bot.add_reaction(message, '\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}')
                    await asyncio.sleep(0.5)
                if int(arg[2]) >= 7:
                    await self.bot.add_reaction(message, '\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}')
                    await asyncio.sleep(0.5)
                if int(arg[2]) >= 8:
                    await self.bot.add_reaction(message, '\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}')
                    await asyncio.sleep(0.5)
                if int(arg[2]) >= 9:
                    await self.bot.add_reaction(message, '\N{DIGIT NINE}\N{COMBINING ENCLOSING KEYCAP}')
                    await asyncio.sleep(0.5)
                if int(arg[2]) == 10:
                    await self.bot.add_reaction(message, '\N{KEYCAP TEN}')
        self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(Poll(bot))
