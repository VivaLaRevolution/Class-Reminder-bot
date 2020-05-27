import discord
from classStuff import classStuff
from discord.ext import commands
import asyncio
from itertools import cycle
import datetime
from User import User
from dotenv import load_dotenv
import os
import time
import CeasarCipher as ceasar
import vingenere_project as vig
import random


load_dotenv()
TOKEN = os.getenv('Token')
bot = commands.Bot(command_prefix='~')



reminder = True
buffer = 5
message_channel_id = 691134148622024776 #announcements
message_channel_id2 = 694951438371258479 #test chat
guildID = 691117560107630625 #2021 server
status = ['Type ~help to find out my commands!','Type ~help to find out my commands!','Type ~help to find out my commands!','Type ~help to find out my commands!', 'TEAR DOWN THE BOURGOISE']
times = classStuff.getTimes()
ADayTimes = times[0]
NormalTimes = times[1]
ENDOFSCHOOL = datetime.time(15,0)
bot.remove_command('help')




#events

@bot.event
async def on_ready():
    global theGuild
    print(f'{bot.user.name} has connected')
    theGuild = bot.get_guild(guildId)

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry but I can't understand what you're saying, are you sure your command was typed correctly?")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("You seem to be missing a part of the command")
    else:
        raise error

@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    channel = message.channel
    if reaction.emoji == '💬':
        await channel.send('eyyyy someone reacted with {}'. format(reaction.emoji))
    
    
    

#commands

@bot.command(name='ID')
async def ID(ctx):
    if checkRole:
        print(ctx.author.mention)
        
@bot.command(name='channelTest')
async def channelTest(ctx):
    print(type(ctx.channel))
    print(ctx.channel)
    print(ctx.channel.category)

@bot.command(name='guilds')
async def guilds(ctx):
    await ctx.send(bot.guilds)
    log('guilds')

@bot.command(name= 'time')
async def getTime(ctx):
    await bot.wait_until_ready()
    time = classStuff.getDateTime('Time')
    await ctx.send(time)
    log('time')

@bot.command(name= 'date')
async def getDate(ctx):
    await bot.wait_until_ready()
    date = classStuff.getDateTime('Date')
    await ctx.send('{} It is an {} day'. format(date, classStuff.findDayType()))
    log('date')

@bot.command(name= 'testMainChannel')
async def testChannel(ctx, role=None):
    if role != None:
        role = discord.utils.get(ctx.guild.roles,name=role)
    BoT = discord.utils.get(ctx.guild.roles, name='Bastards on Time')
    await bot.wait_until_ready()
    message_channel = bot.get_channel(message_channel_id)
    print('connected to channel!')
    await message_channel.send('hey @{} Is this the channel I should be posting in?'. format(BoT.mention))
    log('testMainChannel')

@bot.command(name='testPing')
async def testPing(ctx, role=None):
    print(role)
    if role==None:
        await ctx.send('Plong')
    else:
        await ctx.send('I am testing to see if I can ping {}'. format(role))
    log('ping')

@bot.command(name= 'settings')
async def settingMenu(ctx, setting = 'skip', toggle = 'skip'):
    global reminder, buffer
    hasRole = await checkRole(ctx,'Bot Admin')
    if setting and toggle == 'skip':
            await generateSettings(ctx)
            return ''
    if hasRole:
        
        if hasRole:
            await bot.wait_until_ready()
            isItNum = isNumber(toggle)
            if not isItNum:
                if toggle.lower() == 'false' or 'true':
                    toggle = strToBool(toggle)
                    if toggle == None:
                        await ctx.send('Thats not a settings that I can be set to')
                        isToggle = False
                    else:
                        isToggle = True
                    if setting == 'reminder' and isToggle:
                        reminder = toggle
                        await generateSettings(ctx)

            elif isItNum:
                if setting == 'buffer':
                    if int(toggle)<=30 and int(toggle)>=1:
                        buffer = int(toggle)
                        await generateSettings(ctx)
                    elif int(toggle)>30:
                        await ctx.send('>_< that setting is too girthy for me!')
                    elif int(toggle)<1:
                        await ctx.send('hah, that puny buffer is too small for me')
    else:
        await ctx.send("I'd love to help you but you don't have the proper role :(")
    log('settings')


@bot.command(name= 'next')
async def nextClass(ctx,identifier):
    if identifier == 'class':
        if classStuff.findDayType() == 'No School':
            await ctx.send('There is no school today')
            isSchool = False
        else:
            isSchool = True
        now = datetime.datetime.now()
        if now.time() > ENDOFSCHOOL:
            await ctx.send('School is over')
            isSchool = False
        timeTill = classStuff.timeTillNextClass(ADayTimes,NormalTimes)
        period = timeTill[1]
        time = timeTill[0]
        classTime = timeTill[2]
        if isSchool:
            if time < 60:
                msg = '{} is starting in about {} minutes at {}'. format(period,time, classTime.strftime('%I:%M'))
                await ctx.send(msg)
            else:
                time = await converTimeMins(time)
                hours = time[0]
                minutes = time[1]
                msg = '{} is starting in about {} hours and {} minutes at {}'. format(period, hours, minutes, classTime.strftime('%I:%M'))
    else:
        await ctx.send("idk what you're talking about")
    log('next {}'. format(identifier))

@bot.command(name= 'help')
async def help(ctx):
    embed = discord.Embed(title='Good Boy', description='A very good boy, here are the commands:', colour=0xff3e96)

    embed.add_field(value='Tells you how much time till your next class', name="**<next class**", inline=False)
    embed.add_field(name="**~settings (which setting) (what value)**", value="Changes my settings but you need to have a special role to do this \n\nOr you can just type ~settings to check my settings", inline=False)
    embed.add_field(name='**~schedule**',value="gives a schedule for class times",inline=False)
    embed.add_field(name='**~start/~stop S.reminders**',value='tells me whether or not I should remind you when a Barstow class starts',inline=False)
    embed.add_field(name='**~start/~stop E.reminders**',value='tells me whether or not I should tell you when the next class is after a class ends',inline=False)
    embed.add_field(name='**~encrypt/~decrypt "(key)" "(text)" (user)**',value='encrypts or decrypts text, make sure you have  " "  around your key and text!\nuser is an optional parameter that will send the key to someone',inline=False)
    
    await ctx.send(embed=embed)
    log('help')

@bot.command(name='setupClass')
async def setupClass(ctx):
    hasRole = await checkRole(ctx,'Bot Admin')
    if hasRole:
        BoT = discord.utils.get(ctx.guild.roles, name='Bastards on Time')

        membersList = ctx.guild.members
        userList = {}

                
        
        for member in membersList:
            profile = User(member, member.roles, member.nick)
            if BoT not in member.roles:
                await member.add_roles(BoT)
            userList.update({str(member.name): profile})
    log('setupClass')

@bot.command(name='schedule')
async def schedule(ctx):
    embed = discord.Embed(title='Schedule for today', description='',color=0xff3e96)
    if classStuff.findDayType() != 'No School':
        schedule = classStuff.findSchedule()

        if classStuff.findDayType() == 'A':
            for item in ADayTimes:
                hour = classStuff.matchPeriod(item[0])
                startTime = item[1]
                endTime = startTime + datetime.timedelta(minutes=30)
                embed.add_field(name=hour,value='from {} to {}'. format(startTime.strftime('%I:%M'), endTime.strftime('%I:%M')), inline=False)
        elif classStuff.findDayType() == 'No School':
            await ctx.send("There's no school today")
        else:
            for item in NormalTimes:
                hour = classStuff.matchPeriod(item[0])
                startTime = item[1]
                endTime = startTime + datetime.timedelta(minutes=40)
                embed.add_field(name=hour,value='from {} to {}'. format(startTime.strftime('%I:%M'), endTime.strftime('%I:%M')), inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("There's no school today")
    log('schedule')


@bot.command(name = 'stop')
async def stop(ctx, what):
    if what == 'S.reminders':
        role = discord.utils.get(ctx.guild.roles, name='Bastards on Time')
        await ctx.author.remove_roles(role)
    elif what == 'E.reminders':
        role = discord.utils.get(ctx.guild.roles, name="So You Couldn't Be Bothered to Remember")
        await ctx.author.remove_roles(role)
    else:
        await ctx.send("I don't quite understand that")
    await ctx.send('{} role removed'. format(str(role)))
    log('stop {}'. format(what))


@bot.command(name='start')
async def start(ctx, what):
    if what == 'S.reminders':
        role = discord.utils.get(ctx.guild.roles, name='Bastards on Time')
        await ctx.author.add_roles(role)
    elif what == 'E.reminders':
        role = discord.utils.get(ctx.guild.roles, name="So You Couldn't Be Bothered to Remember")
        await ctx.author.add_roles(role)
    else:
        await ctx.send("I don't quite understand that")
    await ctx.send('{} role added'. format(str(role)))
    log('start {}'. format(what))

@bot.command(name='encrypt')
async def encrypt(ctx,key=None,text=None,user=None):
    await ctx.message.delete()
    person = ctx.author
    if key == None or text == None:
        await ctx.send("You need to add a key and the text you're sending")
    else:
        if isNumber(key) and 0<int(key)<93:
            key = int(key)
            ctext = ceasar.ceasar(text, 'encrypt', key)
        elif key.lower() == 'stream':
            key = ''
            charset = [chr(i) for i in range(32, 127)]
            charset.remove('`')
            charset.remove('"')
            
            for letter in range(len(text)):
                num = random.randint(0,93)
                char = charset[num]
                key += char
            ctext = vig.encrypt(text,key)
                
        else:
            ctext = vig.encrypt(text,key)
        if person.dm_channel == None:
            await person.create_dm()
        dmContent = 'Here is your encrypted text **{}** the key is {}'. format(ctext,key)
        await person.dm_channel.send(dmContent)
        genContent = 'Here is the encrypted text **{}** from {}'. format(ctext,person.mention)
        await ctx.send(genContent)
        if user == None:
            pass
        else:
            user = stripToNum(user)
            user = int(user)
            user = theGuild.get_member(user)
            
            if user.dm_channel == None:
                await user.create_dm()
            userDmContent = '{} just sent an encrypted message in {} for you, the key is **{}**'. format(ctx.author,ctx.channel.name,key)
            await user.dm_channel.send(userDmContent)

@bot.command(name='decrypt')
async def decrypt(ctx,key=None,text=None):
    await ctx.message.delete()
    person = ctx.author
    if key == None or text == None:
        await ctx.send("You need to add a key and the text you're sending")
    else:
        if isNumber(key) and 0<int(key)<95:
            key = int(key)
            dtext = ceasar.ceasar(text, 'decrypt', key)
        else:
            dtext = vig.decrypt(text, key)
        if person.dm_channel == None:
            await person.create_dm()
        dmContent = 'Here is your decrypted text **{}** the key is {}'. format(dtext,key)
        await person.dm_channel.send(dmContent)
        

@bot.command(name='delete')
async def deletee(ctx,time=0):
    if await checkRole(ctx, 'Bot Admin'):
        await asyncio.sleep(time)
        await ctx.message.delete()
        print(ctx.message)
    else:
        await ctx.send("Sorry but you don't have the right role")

@bot.command(name = 'loopMention')
async def loopMention(ctx, role, times, extreme='no'):
    try:
        if role == '<@!374952830701797387>':
            await ctx.send('I would never do that to my creator!')
            
        else:
            
            if await checkRole(ctx,'Bot Admin'):
                await ctx.send('Gotcha')
                if extreme.lower() == 'extreme':
                    channels = ctx.guild.channels
                    textChannels = []
                    for channel in channels:
                        if str(channel.category) == 'Text Channels':
                            textChannels.append(channel)
                        if str(channel) == 'meme':
                            textChannels.remove(channel)
                    for n in range(int(times)):
                        channel = random.choice(textChannels)
                        await channel.send('Hey {}'. format(role))
                else:
                    for n in range(int(times)):
                        await ctx.send('Hey {}'. format(role))
            else:
                await ctx.send("Sorry but you don't have the right role")
    except ValueError:
        await ctx.send('invalid input')

@bot.command(name = 'send')
async def send(ctx,channelOruser,msg):
    await ctx.message.delete()
    user = False
    channel = False

    channels = ctx.guild.channels
    if len(stripToNum(channelOruser)) > 5:
        user = channelOruser
    else:
        channel = channelOruser
    if user != False:
        user = int(stripToNum(user))
        user = ctx.guild.get_member(user)
        if user.dm_channel == None:
                await user.create_dm()
        await user.dm_channel.send(msg)
    if channel != False:
        channelName = channel

        for channel in channels:
            if str(channel) == channelName:
                sendingChannel = channel
                found = True
        if found:
            await sendingChannel.send(msg)
        else:
            await ctx.send('channel not found')

@bot.command(name = 'quote')
async def quoteDay(ctx, ide = None):
    if ide == 'book':
        start = datetime.datetime(2020,5,16,0,0,0)
        now = datetime.datetime.now()
        diff = now - start
        diff = str(diff)
        diffSTR = ''
        for a in diff:
            if a == ',':
                break
            diffSTR += a
        await ctx.send('The quote book has been going on for {}'. format(diffSTR))
    if ide == 'random':
        channel = bot.get_channel(711411574279241799)
        msgList = []
        async for message in channel.history(limit = 1000):
            msgList.append(message)
        newMsg = random.choice(msgList)
        await ctx.send('Here is a random quote: "{}"'. format(newMsg.content))




#Background tasks

async def classCheck():
    await bot.wait_until_ready()
    message_channel = bot.get_channel(message_channel_id)
    message_channel2 = bot.get_channel(message_channel_id2)
    testMessageSent = False
    
    while reminder and not bot.is_closed() and classStuff.findDayType() != 'No School':
        if not testMessageSent:
            await message_channel2.send("i'm checking for class times")
            testMessageSent = True       
        isItTime = classStuff.timeCheck(buffer,ADayTimes,NormalTimes)
        isTime = isItTime[0]
        
        if isTime:
            classPeriod = isItTime[1]
            classTime = isItTime[2]
            if classStuff.findDayType() == 'A':
                classLength = datetime.timedelta(minutes=30)
            else:
                classLength = datetime.timedelta(minutes=40)
            classEnd = classTime + classLength
            BoT = discord.utils.get(theGuild.roles, name='Bastards on Time')
            E_reminder = discord.utils.get(theGuild.roles, name="So You Couldn't Be Bothered to Remember")
            await message_channel.send('{} About {} minutes left till {}, {} will end at {}!'. format(BoT.mention, buffer, classPeriod, classPeriod, classEnd.strftime('%I:%M')))
            if classStuff.findDayType() == 'A':
                sleepMins=30
            else:
                sleepMins=40
            log('start class check')
            await asyncio.sleep(sleepMins*60+buffer*60)
            nextClass = classStuff.timeTillNextClass(ADayTimes,NormalTimes)

            closestTime = nextClass[2].strftime('%I:%M')
            if nextClass[0] < 30:
                ending = 'chop chop!'
            else:
                ending = "you've got some time to relax"
            await message_channel.send('{} {} just ended and {} is starting in {} minutes at {} so {}'. format(E_reminder.mention, classPeriod, nextClass[1], nextClass[0],closestTime, ending))
            log('end class check')
        await asyncio.sleep(30)

async def timeRefresh():
    global ADayTimes,NormalTimes
    times = classStuff.getTimes()
    ADayTimes = times[0]
    NormalTimes = times[1]
    print('Time refreshed')
    await asyncio.sleep(300)

async def change_status():    
    await bot.wait_until_ready()
    msgs = cycle(status)
    while not bot.is_closed():
        current_status = next(msgs)
        await bot.change_presence(activity=discord.Game(name=current_status))
        await asyncio.sleep(60)

async def saySomething():
    while True:
        channelName = input('Select channel: ')
        channels = theGuild.channels
        for channel in channels:
            if str(channel) == channelName:
                sendingChannel = channel
                found = True
        if found:
            print('Channel found!')
            msg = input('what do you wanna say? ')
            await sendingChannel.send(msg)
        else:
            print('channel not found')
        


#helpful functions

async def convertTimeMins(minutes):
    hours = 0
    while minutes >= 60:
        hours += 1
        minutes = minutes - 60
    return hours, minutes

async def checkRole(ctx,role):
    role = discord.utils.get(ctx.guild.roles, name=role)
    if role in ctx.author.roles:
        return True
    else:
        return False

def strToBool(val):
    if val.lower() in ['yes', 'yea', 'true', 'yep', 'ye', 'y', 'sure', 'ok']:
        return True
    elif val.lower() in ['no', 'false', 'nope', 'nah', 'n']:
        return False

def isNumber(val):
    try:
        int(val)
        return True
    except ValueError:
        return False

def stripToNum(string):
    s = ''
    for item in string:
        if isNumber(item):
            s += item
    return s

def log(what):
    time=datetime.datetime.now()
    print('{} called at {}'. format(what,time.strftime('%I:%M')))

async def generateSettings(ctx):
    settingsList = [('reminder',reminder), ('buffer',buffer)]
    embed = discord.Embed(title='My settings are: ', description='settings menu:', colour=0xff3e96)
    for item in settingsList:
        string = '{} is set to '. format(item[0])
        embed.add_field(name=string, value=item[1],inline=False)
    await ctx.send(embed=embed)

async def checkForQuote(message):
    speechBubble = "\u1F4AC"
    reactions = message.reactions
    for re in reactions:
        if re == speechBubble:
            await ctx.send("{0} reacted with the {1.emoji} emoji!".format(message.author.name, re)


bot.loop.create_task(classCheck())
bot.loop.create_task(timeRefresh())
bot.loop.create_task(change_status())
bot.run(TOKEN)







