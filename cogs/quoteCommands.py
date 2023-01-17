#quoteCommands.py

import discord
from discord.ext import commands
from dataclasses import dataclass
import random as randomPY
import asyncio
import math
import os

from commandFunctions import add_quote, search_quotes, get_quote, count_quotes
from sqlFunctions import create_db_connection, execute_query

import config

quoteColour = 0x12AEDE

@dataclass
class Quote:
    quote: str
    author: str

class quoteCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    async def add(self, ctx, quote, author):
        """Adds a quote to the bot's database."""

        if(quote == "" or author == ""):
            await ctx.send('This command is formatted wrong. Please format it as `!add "quote" "author"`')
            return

        if len(quote) > 256:
            await ctx.send(f'Your quote is longer than 256 characters and is unable to be processed :(')
            return
        if len(author) > 256:
            await ctx.send(f'Your author\'s name is longer than 256 characters and is unable to be processed :(')
            return

        try:
            add_quote(Quote(quote, author), ctx.guild.id)
        except:
            await ctx.send('shove off, this thing no work yet')
            return

        embed = discord.Embed(title = f'"{quote}"', description = f'-{author}', color = quoteColour)
        await ctx.send(f'quote added!')
        await ctx.send(embed = embed)

    @commands.hybrid_command()
    async def random(self, ctx, *, search = ""):
        """Returns a random quote from the bot's database."""
        if search != "":
            searchQuotes = search_quotes(search, ctx.guild.id)
            if searchQuotes == 0:
                await ctx.send('There are no quotes added to this server, add some before trying to use this command')

            if len(searchQuotes) < 2:
                await ctx.send('There are not enough quotes in this search to pick a random one :/')
                return

            quoteIndex = randomPY.randint(0, len(searchQuotes) - 1)

            quoteID = searchQuotes[quoteIndex]
            quoteID = quoteID[0]

            embed = discord.Embed(title = f'"{get_quote(quoteID, ctx.guild.id).quote}"', description = f'-{get_quote(quoteID, ctx.guild.id).author}', color = quoteColour)
            await ctx.send(embed = embed)
        else:
            if count_quotes(ctx.guild.id) == 0:
                await ctx.send('There are no quotes added to this server, add some before trying to use this command')
                return

            quoteID = randomPY.randint(1, count_quotes(ctx.guild.id))

            embed = discord.Embed(title = f'"{get_quote(quoteID, ctx.guild.id).quote}"', description = f'-{get_quote(quoteID, ctx.guild.id).author}', color = quoteColour)
            await ctx.send(embed = embed)
        print(f'Random quote sent in channel "{ctx.channel.name}", "{ctx.guild.name}" with search "{search}"')

    @commands.hybrid_command()
    async def get(self, ctx, *, search):
        """Returns every quote in the bot's database that matches a certain keyword"""
        searchQuotes = search_quotes(search, ctx.guild.id)
        if searchQuotes == 0:
            await ctx.send('There are no quotes added to this server, add some before trying to use this command')
            return

        if len(searchQuotes) == 0:
            await ctx.send('There are no quotes that come up when I search this :/')
            return

        addedQuotes = 11

        pageCount = math.ceil((len(searchQuotes) - 1)/10)

        if pageCount == 0:
            pageCount = 1

        messageContent = []
        embed = discord.Embed(title = f'Quotes - Part 1/{pageCount}', description = f'Search: {search}', color = quoteColour)
        for i in range(len(searchQuotes)):
            quoteID = searchQuotes[i]
            quoteID = quoteID[0]

            if addedQuotes % 10 == 0:
                messageContent.append(embed)
                embed = discord.Embed(title = f'Quotes - Part {str(int(addedQuotes / 10))}/{pageCount}', description = f'Search: {search}', color = quoteColour)

            embed.add_field(name = f'"{get_quote(quoteID, ctx.guild.id).quote}"', value = f'-{get_quote(quoteID, ctx.guild.id).author}', inline = False)
            addedQuotes += 1
        messageContent.append(embed)

        messagePlace = 0
        message = await ctx.send(embed = messageContent[messagePlace])

        await message.add_reaction('\u23ee')
        await message.add_reaction('\u25c0')
        await message.add_reaction('\u25b6')
        await message.add_reaction('\u23ed')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['\u25c0', '\u25b6', '\u23ee', '\u23ed']

        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout = 60, check = check)
                if str(reaction.emoji) == '\u25b6' and messagePlace != len(messageContent) - 1:
                    messagePlace += 1
                    await message.edit(embed = messageContent[messagePlace])
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == '\u25c0' and messagePlace > 0:
                    messagePlace -= 1
                    await message.edit(embed = messageContent[messagePlace])
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == '\u23ee':
                    messagePlace = 0
                    await message.edit(embed = messageContent[messagePlace])
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == '\u23ed':
                    messagePlace = len(messageContent) - 1
                    await message.edit(embed = messageContent[messagePlace])
                    await message.remove_reaction(reaction, user)
                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                break
        await ctx.send(f'Get command for search "{search}" has timed out and the reactions will no longer work. Please use the command again if you want to scroll through the pages again')
        print(f'get command used in channel "{ctx.channel.name}", "{ctx.guild.name}" with search "{search}"')

    @commands.hybrid_command()
    async def data(self, ctx):
        """Returns a list of all quotes in a .data file."""
        await ctx.send("Generating data file from quotes database. Depending on the size of the quotes database, this may take a while.")

        connection = create_db_connection(config.dbHost, config.dbUser, config.dbPasswd, config.dbName)

        sID = "sID" + str(ctx.guild.id)
        sql_command = f"select * from {sID}"
        results = execute_query(connection, sql_command, 1)

        output = ""

        for i in results:
            quote = f'{i[0]}, "{i[1]}", "{i[2]}"'
            quote = quote.replace("\n", "!!NEW_LINE!!")
            quote += '\n'

            output += quote

        f = open("quotes.data", "w")
        f.write(output)
        f.close()
        await ctx.send('Full quotes list in format: id, "quote", "author"', file=discord.File('quotes.data'))
        os.remove("quotes.data")
        connection.close()
        
        print(f'Quotes data file sent in channel "{ctx.channel.name}", "{ctx.guild.name}"')

async def setup(client):
    await client.add_cog(quoteCommands(client))