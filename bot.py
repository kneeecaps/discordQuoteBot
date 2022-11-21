# bot.py

import os
import discord
from discord.ext import commands
import time
import random as randomPY
import math
import asyncio

from dataclasses import dataclass

quotes = []
quoteColour = 0x12AEDE
helpColour = 0xFF6600

@dataclass
class quote:
    quote: str
    author: str

def find_nth(string, substr, n):
    if n == 0:
        return
    elif n == 1:
        return string.find(substr)
    else:
        return string.find(substr, find_nth(string, substr, n - 1) + 1)

def load_quotes():
    with open('quotes.data', 'r') as f:
        for line in f:
            quoteStart = find_nth(line, '"', 1) + 1
            quoteEnd = find_nth(line, '"', 2)
            authorStart = find_nth(line, '"', 3) + 1
            authorEnd = find_nth(line, '"', 4)

            nQuote = quote(line[quoteStart:quoteEnd], line[authorStart:authorEnd])

            nQuote.quote = nQuote.quote.replace('!!NEW_LINE!!', '\n')

            quotes.append(nQuote)

def add_quote(quote):
    quotes.append(quote)
    print(f'Quote added: "{quote.quote}", {quote.author}')
    quote.quote = quote.quote.replace('\n', '!!NEW_LINE!!')
    with open('quotes.data', 'a') as f:
        f.write(f'"{quote.quote}" "{quote.author}"\n')

with open('TOKEN.txt', 'r') as f:
    for line in f:
        TOKEN = line

client = commands.Bot(intents=discord.Intents.all(), command_prefix = '!')

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')
    load_quotes()
    print('Quotes have been loaded!')

    activity = discord.Game(name = 'Quoting LITERALLY everything')
    await client.change_presence(status = discord.Status.idle, activity = activity)

@client.command()
async def ping(ctx):
    print(f'Ping command used in channel "{ctx.channel.name}", "{ctx.guild.name}"')
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def add(ctx):
    ctx.message.content = ctx.message.content.replace('“', '"')
    ctx.message.content = ctx.message.content.replace('”', '"')
    ctx.message.content = ctx.message.content.replace('‘', '\'')
    ctx.message.content = ctx.message.content.replace('’', '\'')

    if (ctx.message.content.count('"') != 4):
        await ctx.send('This command is formatted wrong. Please format it as `!add "quote" "author"`')
        return
    if '!!NEW_LINE!!' in ctx.message.content:
        await ctx.send('A quote cannot contain the string "!!NEW_LINE!!" because this is an escape code. Please rewrite the quote without this')
        return

    quoteStart = find_nth(ctx.message.content, '"', 1) + 1
    quoteEnd = find_nth(ctx.message.content, '"', 2)
    authorStart = find_nth(ctx.message.content, '"', 3) + 1
    authorEnd = find_nth(ctx.message.content, '"', 4)

    if ctx.author.id != 851925229374537768:
        add_quote(quote(ctx.message.content[quoteStart:quoteEnd], ctx.message.content[authorStart:authorEnd]))

    embed = discord.Embed(title = f'"{ctx.message.content[quoteStart:quoteEnd]}"', description = f'-{ctx.message.content[authorStart:authorEnd]}', color = quoteColour)
    await ctx.send(f'Quote added!')
    await ctx.send(embed = embed)

@client.command()
async def random(ctx):
    if len(ctx.message.content) > 7:
        searchQuotes = []

        search = ctx.message.content[ctx.message.content.find(' ') + 1:]

        for i in quotes:
            if search.upper() in i.author.upper() or search.upper() in i.quote.upper():
                searchQuotes.append(i)

        if len(searchQuotes) < 2:
            await ctx.send('There are not enough quotes in this search to pick a random one :/')
            return

        quoteIndex = randomPY.randint(1, len(searchQuotes) - 1)

        embed = discord.Embed(title = f'"{searchQuotes[quoteIndex].quote}"', description = f'-{searchQuotes[quoteIndex].author}', color = quoteColour)
        await ctx.send(embed = embed)
    else:
        quoteIndex = randomPY.randint(1, len(quotes) - 1)

        embed = discord.Embed(title = f'"{quotes[quoteIndex].quote}"', description = f'-{quotes[quoteIndex].author}', color = quoteColour)
        await ctx.send(embed = embed)
    print(f'Random quote sent in channel "{ctx.channel.name}", "{ctx.guild.name}"')

@client.command()
async def get(ctx):
    searchQuotes = []

    search = ctx.message.content[ctx.message.content.find(' ') + 1:]

    for i in quotes:
        if search.upper() in i.author.upper() or search.upper() in i.quote.upper():
            verify = 1;

            for j in searchQuotes:
                if i.quote == j.quote:
                    verify = 0

            if verify == 1:
                searchQuotes.append(i)

    if len(searchQuotes) == 0:
        await ctx.send("There are no quotes that come up when I search this :/")
        return

    addedQuotes = 11

    pageCount = math.ceil((len(searchQuotes) - 1)/10)
    messageContent = []
    embed = discord.Embed(title = f'Quotes - Part 1/{pageCount}', description = f'Search: {search}', color = quoteColour)

    for i in searchQuotes:
        if addedQuotes % 10 == 0:
            messageContent.append(embed)
            embed = discord.Embed(title = f'Quotes - Part {str(int(addedQuotes / 10))}/{pageCount}', description = f'Search: {search}', color = quoteColour)
        embed.add_field(name = f'"{i.quote}"', value = f'-{i.author}', inline = False)
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
            reaction, user = await client.wait_for('reaction_add', timeout = 60, check = check)
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

    await ctx.send(f'Get command for search "{search}" has timed out and the reactions will no longer work. Please use the command again if you want to scroll throught the pages again')

    print(f'get command used in channel "{ctx.channel.name}", "{ctx.guild.name}"')

@client.command()
async def data(ctx):
    await ctx.send('Full quotes list:', file=discord.File('quotes.data'))
    print(f'Quotes data file sent in channel "{ctx.channel.name}", "{ctx.guild.name}"')

client.remove_command('help')
@client.command()
async def help(ctx):
    embed = discord.Embed(title = 'Quote Bot Commands', description = 'List of commands for quote bot', color = helpColour)
    embed.add_field(name = '!help', value = 'Shows this message.', inline = False)
    embed.add_field(name = '!add', value = '''Adds a quote to the bot.\n
        The quote cannot have any double quotes (") in it.\n
        It does not matter how this command is sent as long as it starts with !add and the quote is before the author.\n
        USAGE: !add "quote" "author"
        ''', inline = False)
    embed.add_field(name = '!random', value = '''Returns a random quote.\n
        A word can be added onto the end to do a search and pick a random from search results.\n
        USAGE: !random, !random porkchops
        ''', inline = False)
    embed.add_field(name = '!get', value = '''Searches for a quote based on a certain keyword.\n
        The keyword can be the name of the person who said the quote or a section of the quote.\n
        USAGE: !get porkchops
        ''', inline = False)
    embed.add_field(name = '!data', value = '''Sends a file with every recorded quote written in it.\n
        The quotes are written in the format of "quote" "author" ande there is one quote per line.\n
        The file extention is ".data" though the quotes are written in plain text so any text editor should be able to read it.
    ''', inline = False)
    embed.add_field(name = 'NOTES', value = '''All commands are case sensitive and use the camel hump naming system.
        ''')

    await ctx.send(embed = embed)
    print(f'Help command sent in channel "{ctx.channel.name}", "{ctx.guild.name}"')

client.run(TOKEN)
