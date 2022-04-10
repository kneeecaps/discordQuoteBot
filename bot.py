# bot.py

import os
import discord
from discord.ext import commands
import random as randomPY
import asyncio
import math

from dataclasses import dataclass

from commandFunctions import add_quote, search_quotes, get_quote, count_quotes, find_nth, restore_quotes

quoteColour = 0x12AEDE
helpColour = 0xFF6600

@dataclass
class quote:
    quote: str
    author: str

with open('TOKEN.txt', 'r') as f:
    for line in f:
        TOKEN = line

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')

    activity = discord.Game(name = 'Quoting LITERALLY everything')
    await client.change_presence(status = discord.Status.idle, activity = activity)

@client.command()
async def ping(ctx):
    print(f'Ping command used in channel "{ctx.channel.name}", "{ctx.guild.name}"')
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def add(ctx):
    if(ctx.message.content.count('"') != 4):
        await ctx.send('This command is formatted wrong. Please format it as `!add "quote" "author"`')
        return

    quoteStart = find_nth(ctx.message.content, '"', 1) + 1
    quoteEnd = find_nth(ctx.message.content, '"', 2)
    authorStart = find_nth(ctx.message.content, '"', 3) + 1
    authorEnd = find_nth(ctx.message.content, '"', 4)

    quoteTxt = ctx.message.content[quoteStart:quoteEnd]
    authorTxt = ctx.message.content[authorStart:authorEnd]

    if len(quoteTxt) > 256:
        await ctx.send(f'Your quote is longer than 256 characters and is unable to be processed :(')
        return
    if len(authorTxt) > 256:
        await ctx.send(f'Your author\'s name is longer than 256 characters and is unable to be processed :(')
        return

    try:
        add_quote(quote(quoteTxt, authorTxt), ctx.guild.id)
    except:
        await ctx.send('shove off, this thing no work yet')
        return

    embed = discord.Embed(title = f'"{ctx.message.content[quoteStart:quoteEnd]}"', description = f'-{ctx.message.content[authorStart:authorEnd]}', color = quoteColour)
    await ctx.send(f'Quote added!')
    await ctx.send(embed = embed)

@client.command()
async def random(ctx):
    if len(ctx.message.content) > 7:
        search = ctx.message.content[ctx.message.content.find(' ') + 1:]

        searchQuotes = search_quotes(search, ctx.guild.id)
        if searchQuotes == 0:
            await ctx.send('There are no quotes added to this server, add some before trying to use this command')

        if len(searchQuotes) < 2:
            await ctx.send('There are not enough quotes in this search to pick a random one :/')
            return

        quoteIndex = randomPY.randint(1, len(searchQuotes) - 1)

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
    print(f'Random quote sent in channel "{ctx.channel.name}", "{ctx.guild.name}"')

@client.command()
async def get(ctx):
    search = ctx.message.content[ctx.message.content.find(' ') + 1:]
    searchQuotes = search_quotes(search, ctx.guild.id)
    if searchQuotes == 0:
        await ctx.send('There are no quotes added to this server, add some before trying to use this command')
        return

    if len(searchQuotes) == 0:
        await ctx.send('There are no quotes that come up when I search this :/')
        return

    addedQuotes = 11

    pageCount = math.ceil((len(searchQuotes) - 1)/10)
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

    await message.add_reaction('\u25c0')
    await message.add_reaction('\u25b6')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['\u25c0', '\u25b6']

    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60, check=check)
            if str(reaction.emoji) == '\u25b6' and messagePlace != len(messageContent) - 1:
                messagePlace += 1
                await message.edit(embed = messageContent[messagePlace])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == '\u25c0' and messagePlace > 0:
                messagePlace -= 1
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
    await ctx.send('Data command is currently not working since it is not configured for Maria yet.')
    #await ctx.send('Full quotes list:', file=discord.File('quotes.data'))
    #print(f'Quotes data file sent in channel "{message.channel.name}", "{message.guild.name}"')

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
        The quotes are written in the format of "quote" "author" and there is one quote per line.\n
        The file extention is ".data" though the quotes are written in plain text so any text editor should be able to read it.\n
        Please note: The data command currently does not support MariaDB, I will eventually fix it though
    ''', inline = False)
    embed.add_field(name = 'NOTES', value = '''All commands are case sensitive and use the camel hump naming system.\n
        Both the quote and the author section of the add command have a limit of 256 characters\n
        ''')

    await ctx.send(embed = embed)
    print(f'Help command sent in channel "{ctx.channel.name}", "{ctx.guild.name}"')

#restore_quotes()

client.run(TOKEN)
