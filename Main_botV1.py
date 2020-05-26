import discord
from classStuff import classStuff
from discord.ext import commands
import asyncio
from itertools import cycle
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('Token')

bot = commands.Bot(command_prefix='<')


reminder = True
buffer = 5
message_channel_id = 691134148622024776 #announcements
message_channel_id2 = 694951438371258479 #test chat
status = ['Type <help to find out my commands!','Type <help to find out my commands!','Type <help to find out my commands!','Type <help to find out my commands!', 'TEAR DOWN THE BOURGOISE']
ADayTimes = classStuff.ADayTimes
NormalTimes = classStuff.NormalTimes
ENDOFSCHOOL = datetime.time(15,0)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected')

@bot.command(name= 'time')
async def getTime(ctx):
    await bot.wait_until_ready()
    time = classStuff.getDateTime('Time')
    await ctx.send(time)


@bot.command(name= 'date')
async def getDate(ctx):
    await bot.wait_until_ready()
    date = classStuff.getDateTime('Date')
    await ctx.send('{} It is an {} day'. format(date, classStuff.findDayType()))

@bot.command(name= 'testMainChannel')
async def testChannel(ctx):
    role = discord.utils.get
    await bot.wait_until_ready()
    message_channel = bot.get_channel(message_channel_id)
    print('connected to channel!')
    await message_channel.send('hey @everyone Is this the channel I should be posting in?')
    

@bot.command(name= 'settings')
async def settingMenu(ctx, setting = 'skip', toggle = 'skip'):
    global reminder, buffer
    role = discord.utils.get(ctx.guild.roles, name='Bot Admin')
    try:
        if setting and toggle == 'skip':
            await generateSettings(ctx)
            return ''
        if role in ctx.author.roles:
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
                    buffer = int(toggle)
                    await generateSettings(ctx)
        else:
            await ctx.send("I'd love to help you but you don't have the proper role :(")
    except discord.ext.commands.errors.MissingRequiredArgument(param):
        await generateSettings(ctx)


@bot.command(name= 'next')
async def nextClass(ctx,identifier):
    if identifier == 'class':
        isSchool = True
        if classStuff.findDayType() == 'No School':
            await ctx.send('There is no school today')
            isSchool = False
        now = datetime.datetime.now()
        if now.time() > ENDOFSCHOOL:
            await ctx.send('School is over')
            isSchool = False
        timeTill = classStuff.timeTillNextClass(ADayTimes,NormalTimes)
        period = timeTill[1]
        time = timeTill[0]
        if isSchool:
            if time < 60:
                msg = '{} is starting in {} minutes'. format(period,time)
                await ctx.send(msg)
            else:
                time = converTimeMins(time)
                hours = time[0]
                minutes = time[1]
                msg = '{} is starting in {} hours and {} minutes'. format(period, hours, minutes)
    else:
        await ctx.send("idk what you're talking about")

@bot.command(name= 'help')
async def help(ctx):
    embed = discord.Embed(title='Good Boy', description='A very good boy, here are the commands:', colour=0xff3e96)

    embed.add_field(value='Tells you how much time till your next class', name="**<next class**", inline=False)
    embed.add_field(name="**<settings (which setting) (what value)**", value="Changes my settings but you need to have a special role to do this \n\nOr you can just type <settings to check my settings", inline=False)

    await ctx.send(embed=embed)

def convertTimeMins(minutes):
    hours = 0
    while minutes >= 60:
        hours += 1
        minutes = minutes - 60
    return hours, minutes


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
        classPeriod = isItTime[1]
        if isTime:
            print('class time should be working')
            await message_channel.send('@everyone About {} minutes left till {}!'. format(buffer, classPeriod))
            await asyncio.sleep(buffer*60)
        await asyncio.sleep(60)

async def change_status():    
    await bot.wait_until_ready()
    msgs = cycle(status)
    while not bot.is_closed():
        current_status = next(msgs)
        await bot.change_presence(activity=discord.Game(name=current_status))
        await asyncio.sleep(60)



def strToBool(val):
    if val.lower() in ['yes', 'yea', 'true', 'yep', 'ye']:
        return True
    elif val.lower() in ['no', 'false', 'nope', 'nah']:
        return False

def isNumber(val):
    try:
        int(val)
        return True
    except ValueError:
        return False
        




async def generateSettings(ctx):
    settingsList = [('reminder',reminder), ('buffer',buffer)]
    embed = discord.Embed(title='My settings are: ', description='settings menu:', colour=0xff3e96)
    for item in settingsList:
        string = '{} is set to '. format(item[0])
        embed.add_field(name=string, value=item[1],inline=False)
    await ctx.send(embed=embed)


bot.loop.create_task(classCheck())
bot.loop.create_task(change_status())
bot.run(TOKEN)






