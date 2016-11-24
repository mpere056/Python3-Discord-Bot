# Python3-Discord-Bot
This is a multipurpose discord bot I made using discord.py and various other libraries.
The main purpose of my bot is to learn how I can use my linux based vps with my bot.

Here's what the bot can do so far:

- Screenshot Webpages
  - Screenshot a specified website, and if asked to, the bot will wait a specified amount of seconds before screenshotting it
  - Usage: screenshot [website] {and wait for [amount of seconds] seconds}
  - Ex. screenshot https://youtube.com and wait 2 seconds
  
- Screenshot Messages
  - Screenshot any message on the discord page, but the bot will not scroll up to screenshot older messages
  - usage: test1 {number of messages above the current message}
  - ex. test1 1 
  
- Assign roles
  - Assign one of the currently existing specified roles to the specified user
  - The bot will attempt to understand normal sentence structures to figure out the role and user
  - ex. give pbot the role Bot

- Execute bash commands
  - Execute any bash command through the vps that runs the bot, which runs on linux
  - Typing after a command will also output anything the bash command outputs in the terminal
  - Usage: bash [command] {-o}
  - ex. bash ls -o

- Return osu signatures
  - Get a link of an osu signature by using Lemmy's osu signature generator
  - Usage: osu [name] [mode]
  - ex. osu pbot mania

- Greentext
  - ex. >you can't greentext on discord?

- Kick people
  - ex. kick pbot
