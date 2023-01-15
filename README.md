# Discord Quote Bot

## About
This is a discord bot I made that can record and keep track of quotes people have said. This was originally made as a bit of a joke between me and my friends so we could take some things said out of context later for some laughs, but I have put the code on github in case anyone else wants to use it for anything.

The bot has two main versions of it, you can get the code for each version from the branches page on github. The first version (in branch main) uses a database to store the quotes as well as prefixes for each server, the second version (in branch textFileVersion) uses a text file instead of a database. The version of the bot that uses a text file is both slower and a bit outdated, but it is much easier to set up and use if you are not too good with technology. This version is a bit outdated because once I was able to get a server that can host the database, I put my full attention to the database version. I have no intention of updating the textFileVersion anymore, but if anyone wanted to port some features over I would probably approve pull requests.

## Setup guide

To get the bot running, you need to do five main things: 
* Download the code for the bot
* Install the dependancies for the bot
* Create a database if you are using the database version or the text file if you are using that version
* Get a token for the bot and store that in the right file
* Start the bot

Here is a basic guide on how to get the bot running: 

1. The first thing you need to do to is download the code from the bot. Download the code from github and extract it into the directory you want the bot to be running from. Make sure the the bot has the required permissions to read and write in the directory you extract it to. If you are running windows, this should be done automatically, for linux users, you should be able to google how to do this and I have no idea how to do it on other operating systems. 

2. Once you have the code downloaded, you need to install the bot's dependancies for it to work. The quote bot's dependancies can be installed with pip by using the syntax `pip install *dependancy_name*`. Make sure you install all of them otherwise it will not work. Here is a list of the bot's dependancies:
  * discord.py
  * asyncio
  * dataclasses
  * mysql-connector-python (only needed if you are using the database version)
  
3. The bot will need a place to store quotes (and prefixes if you are using the database version) so now is the time to set that up. I will explain how to do this for both versions here. 

  * If you are using the text file version, just make a file in the directory the code is in called `quotes.data` and you should be done. 

  * If you are using the database version, in config.py four variables set to the credentials needed for the database are declared. Everytime database credentials are needed in the code they are retrieved from this file. You can configure your database to work with these credentials if you want (although using user as both the username and password isn't very secure), or you can change those values to whatever you need them to be. Once you have made a database that the bot has access to and configured the credentials in config.py, the last thing you need to do is create a table in that database to store server prefixes. The bot will automatically create tables for quotes, but it will not do it automatically for prefixes. I used the command `CREATE TABLE prefixes ( sID varchar(255) PRIMARY KEY NOT NULL, prefix varchar(10) NOT NULL );` to create this table for me, you can use it too but if you really wanted to save space you can lower the amount of data reserved for each column. The bot will not add any prefix longer than 3 characters but this table has space for 10 and I am pretty sure there aren't any server ids that are 255 characters long, if you want you can change this but what I put above is what I have tested to work. 

4. Next, you need to get a token for your bot. You get this from the [Discord Developer Page](https://discord.com/developers/applications) by creating an application and going to the bot tab. If you need more help with this, any guide about how to make a discord bot will have images and more in depth details on how to do this. While you are on this page, it is also good to invite the bot to a test server from the oauth2 tab. Again, if you are having trouble with this any guide on how to make a bot will have more details.

5. Finally, just start the bot. Using a command line, navigate to the directory where you put the bot's code and run the command `python bot.py`. If you have done everything right, within a few seconds it should tell you that the bot is online and you should see it pop up in your server. If this command spits out an error, you have most likely forgotten to install a dependancy or messed up the configuration of the database. I would also recommend running a few of the commands in a test server, because if the database is configured incorrectly you may not notice until a certain command is run. If you have any trouble with this configuration, just create an issue on github and I can try to help you fix it. 
