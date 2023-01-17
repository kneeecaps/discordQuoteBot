# bot.py

import os
import discord
from discord.ext import commands

from commandFunctions import restore_quotes
from sqlFunctions import create_db_connection, execute_query

import config

with open('TOKEN.txt', 'r') as f:
    for line in f:
        TOKEN = line

def get_prefix(client, ctx):
    connection = create_db_connection(config.dbHost, config.dbUser, config.dbPasswd, config.dbName)
    sql_command = f"""SELECT prefix FROM prefixes WHERE sID = '{ctx.guild.id}';"""

    prefix = execute_query(connection, sql_command, 2)

    if(not prefix):
        prefix = '!'
    else:
        prefix = prefix[0]

    connection.close()
    return prefix


class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = get_prefix,
            intents = discord.Intents.all(),
        )

    async def setup_hook(self):
        client.remove_command('help')

        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                await client.load_extension("cogs." + f[:-3])

client = Client()

#uncomment this if you want to add quotes from the text file version to a sql database
#Make sure you configured server id in the function definition in commandFunctions.py first
#restore_quotes() 

client.run(TOKEN)
