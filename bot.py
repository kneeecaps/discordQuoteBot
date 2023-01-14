# bot.py

import os
import discord
from discord.ext import commands

from commandFunctions import restore_quotes

with open('TOKEN.txt', 'r') as f:
    for line in f:
        TOKEN = line

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = '!',
            intents = discord.Intents.all(),
        )

    async def setup_hook(self):
        client.remove_command('help')
        await client.load_extension("commands")


client = Client()

#restore_quotes()

client.run(TOKEN)
