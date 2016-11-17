import discord
import asyncio
import os
import random
from selenium import webdriver
from time import sleep
from PIL import Image

client = discord.Client()
token = "" # Token used to connect to the bot
logs = [] # Records all message the bot receieves
browser = webdriver.Firefox() # Opens a browser with selenium
browser.maximize_window()
admins = [] # List of users with access to certain commands


#Send an image of the discord message specified
#Thanks to RandomPhobia
def screenshot_message(message):
		tempk = message.content.split(" ")
		templ = "https://discordapp.com/channels/" + str(message.server.id) + "/" + str(message.channel.id)
		browser.get(templ)
		sleep(1)
		#element = browser.find_element_by_id('yt-masthead-logo-fragment') # find part of the page you want image of
		elements = browser.find_elements_by_css_selector(".message-group.hide-overflow")
		if (message.content == "test1"):
			element = elements[len(elements)-1]
		else:
			element = elements[len(elements)-1-int(tempk[1])]
		location = element.location
		size = element.size
		browser.save_screenshot('screenshot.png') # saves screenshot of entire page
		#browser.quit()

		im = Image.open('screenshot.png') # uses PIL library to open image in memory

		left = location['x']
		top = location['y']
		right = location['x'] + size['width']
		bottom = location['y'] + size['height']

		im = im.crop((left, top, right, bottom)) # defines crop points
		im.save('screenshot.png')
		yield from client.send_file(message.channel, "screenshot.png")


#Send an image of an osu signature
#Based on username and mode specified
#Thanks to Lemmy's osu signature generator
def osu(message):
        temp = message.content.split(" ")
	tempn = ""
	if (temp[2] == "taiko"):
		tempn = "1"
	elif (temp[2] == "ctb"):
		tempn = "2"
	elif (temp[2] == "mania"):
		tempn = "3"
	tempm = "http://lemmmy.pw/osusig/sig.php?colour=pink&uname=" + temp[1] + "&mode=" + tempn
	yield from client.send_message(message.channel, tempm)


#Screenshots the entire page after waiting a specified amount of seconds
def screenshot(message):

        tempm = message.content.split(" ")
	browser.get(tempm[1])
	sleep(1) #Always waits at least 1 second to let the page load
	
	#Checks if the user specifies an amount of seconds to wait
	if ("wait" in message.content or "sleep" in message.content):
		temps = 0
		if (not("second" in message.content)):
			for z in range(0, len(tempm)):
				if (tempm[z] == "wait" and tempm[z+1] != "for"):
					temps = int(tempm[z+1])
				else:
					temps = int(tempm[z+2])
		else:
			for z in range(0, len(tempm)):
				if ("second" in tempm[z]):
					temps = int(tempm[z-1])
		sleep(temps)
		
	browser.save_screenshot("test.png")
	yield from client.send_file(message.channel, "test.png")


#Sends a message in greentext by using disord's javascript format
def greentext(message):
        tempm = message
	tempn = str(message.author)
	temps = message.content.replace("\"", "'")
	temps = temps.replace(">", "\">").replace("\n", "\"\n\">").replace("\"\"", "\"")
	while ("\">\">" in temps):
		temps = temps.replace("\">\">", "\">")
	while ("\"> \">" in temps):
		temps = temps.replace("\"> \">", "\">")
	yield from client.delete_message(message)
	yield from client.send_message(tempm.channel, "```js\n" + temps + "\"\n```")


#Assigns a role to the specified user using realistic commands
def add_role(message):

	tempr = []
	text = message.content.split(" ")
	textr = ""
	texta = ""
	textm = ""
	done = "no"
	me = "false"
	
	#Realistic syntax checking for name and role
	if (text[len(text)-2] == "to"):
		texta = text[len(text)-1]
	else:
		texta = text[1]
	for z in range(0, len(text)):
		if (text[z] == "give" and done == "no"):
			texta = text[z + 1]
		if (text[z] == "named" or text[z] == "name"):
			texta = text[z + 1]
			done = "yes"
		if (text[z] == "me"):
			me = "true"
		if (text[z] == "role"):
			textr = text[z + 1]
	
	#Getting the discord.py member from specified name
	for z in message.server.members:
		if (texta in z.name):
			textm = z
			
	#Getting the role from specified name
	for z in range (0, len(message.server.roles)):
		if (textr in message.server.roles[z].name):
			tempr.append(message.server.roles[z])
			
	if (me == "true"):
		yield from client.add_roles(message.author, tempr[0])
	else:
		yield from client.add_roles(textm, tempr[0])
		yield from client.send_message(message.channel, "Added role " + tempr[0].name + " to " + textm.name)


#Kicks the specified user and logs it in a logs channel
def kick(message):
	text = message.content.split(" ")
	textn = ""
	for z in range(0, len(text)):
		if (text[z] == "kick"):
			textn = text[z+1]
	for z in message.server.members:
		if(textn in z.name):
			textn = z
			break
	yield from client.kick(z)
	for z in message.server.channels:
		if ("log" in z.name):
			yield from client.send_message(z, message.author.name + " kicked " + textn.name)
			break

@client.event
@asyncio.coroutine
def on_message(message):
	#Record every message the bot receives
	logs.append(message)
        
	#Sends an image of the specified discord message
	#ex. test1 3
	#The command above will send a screenshot of the 3rd message from the bottom
        if ("test1" in message.content[0:6]):
                screenshot_message(message)
        
	#Sends an osu signature made by Lemmy
	#ex. osu pbot taiko
        if ("osu " in message.content[0:3]):
		osu(message)
        
	#Sends a screenshot of a webpage
	#ex. screenshot https://youtube.com and wait 3 seconds
	if ("screenshot" in message.content[0:10]):
                screenshot(message)

	#Greentexting
	#ex. >you can't greentext on discord?
	if (message.content[0] == ">" and message.author != client.user):
		greentext(message)
                
	#non public commands		
	elif (str(message.author) in admins):
		
		#Assigns a role to a user using realistic commands
		#ex. assign the role user to pbot
		#ex. give pbot the role user
		if ("role" in message.content):
			add_role(message)

		#Kicks the specified user
		if ("kick" in message.content):
			kick(message)

		#Uses my vps to perform bash commands and return the output if specified
		#ex. bash ls -o
		#The above command will output the content of current directory
		elif ("bash" in message.content):
			if (message.content[-2:] == "-o"):
				os.system(message.content[5:-2] + " > temp.txt")
				t = open("temp.txt")
				yield from client.send_message(message.channel, t.read())
			else:
				os.system(message.content[5:])
				
		#Outputs the effects of the last bash command				
		elif (message.content == "output"):
			t = open("temp.txt")
			yield from client.send_message(message.channel, str(t.read()))				
		
		#Uses my vps to write code in python				
		elif (message.content[0:6] == "python"):
			os.system("echo \"" +  message.content[7:] + "\" >> python.python")
		
		#Runs previously written python code
		elif (message.content == "run"):
			os.system("echo \"\" > temp.txt")
			os.system("python3 python.python >> temp.txt")
			t = open("temp.txt")
			yield from client.send_message(message.channel, t.read())			
		
	#Prints every message received in the terminal
	print(str(message.author) + ": " + message.content)

#Connects to the bot
client.run("token")
