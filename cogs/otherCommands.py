#otherCommands.py

import discord
from discord.ext import commands

from sqlFunctions import create_db_connection, execute_query

import config

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
    async def prefix(self, ctx, new_prefix):
        """Changes the prefix of the bot"""

        if(len(new_prefix) > 3):
            await ctx.send("New prefix is too long. Try a shorter one.")
            return

        connection = create_db_connection(config.dbHost, config.dbUser, config.dbPasswd, config.dbName)
        sql_command = f"""SELECT prefix FROM prefixes WHERE sID = '{ctx.guild.id}';"""

        prefix = execute_query(connection, sql_command, 2)

        if(not prefix):
            sql_command = f"""INSERT INTO prefixes (sID, prefix) VALUES ('{ctx.guild.id}', '{new_prefix}');"""
        else:
            sql_command = f"""UPDATE prefixes SET prefix = '{new_prefix}' WHERE sID = '{ctx.guild.id}';"""

        execute_query(connection, sql_command, 0)
        connection.close()

        await ctx.send(f'Prefix successfully changed to "{new_prefix}"')

    @commands.hybrid_command()
    async def ping(self, ctx):
        """Returns the ping of the bot."""
        print(f'Ping command used in channel "{ctx.channel.name}", "{ctx.guild.name}"')
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.hybrid_command()
    async def help(self, ctx):
        """Explains the functions of each command."""
        embed = discord.Embed(title = 'Quote Bot Commands', description = 'List of commands for quote bot', color = helpColour)
        embed.add_field(name = '!help', value = 'Shows this message.', inline = False)
        embed.add_field(name = '!add', value = '''Adds a quote to the bot.\n
            Quotes spanning multiple lines will not work if you use / commands. Use prefix commands for these quotes.\n
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
            The quotes are written in the format of {id, "quote", "author"} and there is one quote per line.\n
            The file extention is ".data" but the quotes are written in plain text so any text editor should be able to read it.\n
        ''', inline = False)
        embed.add_field(name = 'NOTES', value = '''All commands are case sensitive and use the camel hump naming system.\n
            Both the quote and the author section of the add command have a limit of 256 characters\n
            ''')

        await ctx.send(embed = embed)
        print(f'Help command sent in channel "{ctx.channel.name}", "{ctx.guild.name}"')

async def setup(client):
    await client.add_cog(otherCommands(client))