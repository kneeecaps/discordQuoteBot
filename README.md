# Discord Quote Bot
This is a discord bot I made because I did not like the bots other people made for the same purpose. This bot records quotes and can then search through these quotes and return quotes that match certain keywords or pick random quotes. The bot is pretty simple and can probably be optimized in many ways, but it works for what I want it to. I made the bot as a form of gateway so that my friends can all access and contribute to a quotes list though you can use it for whatever you see fit.

Included in this repository is the code for the bot, the image I am using as the bots profile picture and a .xcf file for if you want to change that picture.

The bot is set up so that is more or less runs out of the box, all you need to do is:

  -Add the bots token as a text file

  -Add a file for the bot to store quotes in (unless you are using the SQL version, then make a database)

  -Install the bots dependencies using pip


PLEASE NOTE THAT THE INSTRUCTIONS BELOW ARE FOR THE BOT TO WORK AS SOON AS POSSIBLE AND WITHOUT MUCH EXTRA EFFORT. THE BOT CAN GET BETTER PERFORMANCE BY COMPLETING A LONGER CONFIGURATION PROCESS BUT I WILL NOT EXPLAIN THAT HERE. 

YOU CAN CHANGE THE NAMES OF THE FILES AND ALL THAT STUFF, BUT YOU WILL HAVE TO MODIFY THE CODE, WHAT IS LISTED BELOW IS JUST WHAT I HAVE USED

Add the bot's token, which you should get from the discord developer website, to a file called `TOKEN.txt`.

The next thing you need to do to set up the bot is to make a file for it to store its quotes in (unless as I stated earlier you are using the SQL version). To do this, you just need to make a file called `quotes.data`.

Then finally, you need to install all the dependencies for the bot. Here is a list of all the dependencies:

  -discord.py

  -asyncio

  -dataclasses

  -mysql-connector-python (only needed if using SQL version)


These can be installed by just running the command `pip install packageName`, for example: `pip install discord.py`. I may have missed one or two dependencies but I think I got them all.

If you are using the SQL version of the bot, you also need to create a database for the bot to read and write to. To do this, you may need to reconfigure the bot. The version of the bot I was using for testing (and the one which is one the repository at the time of writing this) is configured to run with a database saved on localhost by the name of `quotes`. I used mariadb to test this as well, though the code should work with most other databases. I would also like to say, that I would not recommend using the SQL version if you don't know at least basic programming. It does need a little more skill than the other version.

If anything in this file is inaccurate please tell me so I can fix it. Also, it is worth noting that a big drawback of the main version of the bot is that it
only supports one quotes list. The SQL version has one quotes list per server, though this does not carry across to the main one.

As a final note, the SQL version to my knowledge has not been updated to include some of the newer features in the other version. This is mainly because the  server I was using to test the SQL version broke. At some point I may update it to include newer features, right now it is working, it just lacks some of the features the other version has.
