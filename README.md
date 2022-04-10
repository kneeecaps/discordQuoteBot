# discordQuoteBot
This is a discord bot I did not like the bots other people made for the same purpose.
This bot records quotes and can then search through these quotes and return quotes that match certain keywords or pick random quotes.
The bot is pretty simple and can probably be optimized in many ways, but it works for what I want it to.
I made the bot as a form of gateway so that my friends can all access and contribute to a quotes list though you can use it for whatever you see fit.

Included in this repository is the code for the bot, the image I am using as the bots profile picture and a .xcf file for if you want to change that picture.

The bot is set up so that is more or less runs out of the box, all you need to do is:
  -Add the bots token a text file
  -Add a file for the bot to store quotes in (unless you are using the SQL version)
  -Install the bots dependencies using pip


PLEASE NOTE THAT THE INSTRUCTIONS BELOW ARE FOR THE BOT TO WORK AS SOON AS POSSIBLE WITH VERY LITTLE FOR YOU
YOU CAN CHANGE THE NAMES OF THE FILES AND ALL THAT STUFF, BUT YOU WILL HAVE TO MODIFY THE CODE, WHAT IS LISTED BELOW IS JUST WHAT I HAVE USED

THESE INSTRUCTIONS ALSO DO NOT COVER THE SQL VERSION, THEY WILL ONLY WORK ON THE ONE STORING QUOTES IN A FILE
I WILL UPDATE IT TO INCLUDE THE SQL VERSION LATER

Add the bot's token, which you should get from the discord developer website, to a file called `TOKEN.txt`.

The next thing you need to do to set up the bot is to make a file for it to store its quotes in (unless as I stated earlier you are using the SQL version).
To do this, you just need to make a file called `quotes.data`.

Then finally, you need to install all the dependancies for the bot.
Here is a list of all the dependancies:

  -discord.py

  -asyncio

  -dataclasses


These can be installed by just running the command `pip install packageName`, for example: `pip install discord.py`.
I may have missed one or two dependancies but I think I got them all.

If anything in this file is inaccurate please tell me so I can fix it. Also, it is worth noting that a big drawback of the main version of the bot is that it 
only supports one quotes list. The SQL version has one quotes list per server, though this does not carry across to the main one.

As a final note, the SQL version to my knowledge has not been updated to include some of the newer features in the other version.
This is mainly because the server I was using to test the SQL version broke.
At some point I may update it to include newer features, right now it is 100% working, it just needs to have some other features added to it.
