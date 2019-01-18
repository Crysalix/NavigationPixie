#!/usr/bin/env python3.5
import asyncio
import json
import random
import time

from discord.ext import commands
from pixie_function import *

class Jokes:

    def __init__(self, bot):
        self.bot = bot

    def __unload(self):
        pass

    @commands.command(pass_context=True)
    async def joke(self, ctx, i=0):
        """Je raconte une blague."""
        if i == 0:
            rand = random.randrange(25)
            await asyncio.sleep(.5)
        else:
            rand = i
        serverlistmodules = readData ('server', ctx.message.author.server.id)
        if serverlistmodules["jokes"]["last"] == "disabled":
            return
        if ctx.message.author.server.id != '258418637948452865':
            if(rand == 0 or rand == 1):
                rand += 2
        if rand == 0:
            await self.bot.say('Hey <@355765834616143893> ! Tu veux entendre une blague sur les paquets TCP ?')
            await asyncio.sleep(2)
            await self.bot.say('Ok ! Je vais te raconter une blague sur les paquets TCP.')
            await asyncio.sleep(2)
            await self.bot.say('Attention, je commence ma blague sur les paquets TCP.')
            await asyncio.sleep(2)
            await self.bot.say('C\'est l\'histoire de... Attend... Tu as timeout je recommence.')
            await asyncio.sleep(.5)
            await self.bot.say('Tu veux entendre une blague sur les paquets TCP ?')
        elif rand == 1:
            await self.bot.say('Knock knock !')
            await asyncio.sleep(2)
            await self.bot.say('Doctor.')
            await asyncio.sleep(3)
            await self.bot.say(':D')
        elif rand == 2:
            await self.bot.say('Une requête TCP entre dans un bar et demande une bière, le barman lui répond :\n`Tu veux une bière ?`\nEt la requête TCP lui répond :\n`Oui, je veux une bière`\nEt la requête a reçu une bière.')
        elif rand == 3:
            await self.bot.say('Une requête UDP entre dans un bar et demande une bière, mais personne ne lui répond.')
        elif rand == 4:
            await self.bot.say('Une addresse IPv4 entre dans un bar, le barman lui dit :\n`Hey ! Est ce que ça va ?`\nEt l\'addresse IPv4 lui répond :\n`Non ! Je suis épuisé !`')
        elif rand == 5:
            await self.bot.say('Une requête AppleTalk entre dans une bière et commande un bar, mais personne ne le comprend.')
        elif rand == 6:
            await self.bot.say('Une requête Multicast entre dans un bar et dit :\n`Une bière pour tout le monde !`\nEt tout le monde reçu une bière instantanément.')
        elif rand == 7:
            await self.bot.say('Un aveugle entre dans un bar, puis dans la table, puis dans une chaise, puis dans le comptoir...')
        elif rand == 8:
            await self.bot.say('Un torrent entre dans un bar avec un verre vide et dit :\n`Je voudrais une bière !`\nEt tout le monde lui verse un peu de sa bière dans le verre du torrent.')
        elif rand == 9:
            await self.bot.say('Une requête SQL entre dans un bar, croise deux potes anglais et leur dit\n`Hey can I JOIN you ?`')
        elif rand == 10:
            await self.bot.say('Deux geeks sont dans un bar, quand d\'un coup le barman tombe devant eux. Un des geeks se lève et crie :\n`OH NON ! Le serveur est down !`')
        elif rand == 11:
            await self.bot.say('Une addresse IPv6 entre dans un bar, le barman lui dit :\n`Hey ! Est ce que ça va ?`\nEt l\'addresse IPv6 lui répond :\n`Non ! Personne ne me comprend !`')
        elif rand == 12:
            await self.bot.say('Je peux vous raconter une blague sur les packet UDP mais je suis pas sûr que vous allez la saisir')
        elif rand == 13:
            await self.bot.say('WHOIS going to tell us a Domain Name joke?')
        elif rand == 14:
            await self.bot.say('2 Computers are talking :\n`How did you like my HTTP 200 joke ?`\n`It was Ok.`')
        elif rand == 15:
            await self.bot.say('The best thing about DNSSEC jokes is that you can check if they were told wrong.')
        elif rand == 16:
            await self.bot.say('La mauvaise chose avec les blagues sur les ipv6 c\'est que personne veut les dire en premier')
        elif rand == 17:
            await self.bot.say('Pourquoi les develloppeurs confondent souvent halloween et noel ?\nParce que OCT 31 = DEC 25')
        elif rand == 18:
            await self.bot.say('What kind of doctor fixes broken websites?\nA URLologist.')
        elif rand == 19:
            await self.bot.say('Une fois, j\'ai recu une blague sur Tor, mais j\'ai jamais su qui me l\'a racontée.')
        elif rand == 20:
            await self.bot.say('Les blagues DHCP marchent uniquement quand elles sont dites par une seule personne.')
        elif rand == 21:
            await self.bot.say('Un paquet ICMP entre dans un bar et dit `Bonjour` au barman. Quand soudain, le barman cours à toute vitesse chez la femme du paquet ICMP et lui dit `Bonjour`')
        elif rand == 22:
            await self.bot.say('Un gars entre dans un bar, et commande un verre.\n`Un whisky pour moi.`\nIl sort un petit bonhomme de 10 cm de sa poche, le pose sur le comptoir et dit :\n`Et un dé à coudre de Whisky pour lui.`\nLe barman les regarde et dit :\n`Où as tu trouvé ce petit bonhomme ?`\nLe grand, en se tournant vers le petit bonhomme, lui dit:\n`Heeeeeeee... C\'est au pérou ou en afrique déjà que tu avais insulté ce sorcier ?`')
        elif rand == 23:
            await self.bot.say('Comment appelle-t-on un chat tombé dans un pot de peinture le jour de Noël ? Un chat-pein de Noël !')
        elif rand == 24:
            await self.bot.say('Un éléphant et une girafe entre dans un bar. Que prennent-ils ?\nBeaucoup de place !')

def setup(bot):
    bot.add_cog(Jokes(bot))
