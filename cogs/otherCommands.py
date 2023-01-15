#otherCommands.py

import discord
from discord.ext import commands

helpColour = 0xFF6600

class otherCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Game(name = 'Quoting LITERALLY everything')
        await self.client.change_presence(status = discord.Status.idle, activity = activity)

        print(f'{self.client.user} has connected to discord!')

    @commands.command()
    async def sync(self, ctx):
        if(ctx.author.id == 365651769805635594):
            await self.client.tree.sync()
            print(f'Synced commands to server: "{ctx.guild.name}"')
            await ctx.send("Synced commands to current server.")
        else: 
            await ctx.send("You cannot do this command.")

    @commands.hybrid_command()
    async def ping(self, ctx):
        """Returns the ping of the bot."""
        print(f'Ping command used in channel "{ctx.channel.name}", "{ctx.guild.name}"')
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.hybrid_command()
    async def data(self, ctx):
        """Returns a list of all quotes in a .data file."""
        await ctx.send('Data command is currently not working since it is not configured for MariaDB yet.')
        #await ctx.send('Full quotes list:', file=discord.File('quotes.data'))
        #print(f'Quotes data file sent in channel "{message.channel.name}", "{message.guild.name}"')

    @commands.hybrid_command()
    async def help(self, ctx):
        """Explains the functions of each command."""
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

async def setup(client):
    await client.add_cog(otherCommands(client))