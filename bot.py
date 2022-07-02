import discord
import random
import re
import os
import json
from discord import guild
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from dotenv import load_dotenv
load_dotenv()
# os.chdir("C:\\Users\\richardbann\\Documents\\PycharmProjects\\doggobot2021")

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True


token = os.getenv("BOT_TOKEN")

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix, intents=intents)

status = cycle(['flippin doggo coins', 'with doggo coins', 'generating more doggo coins', 'eating doggo coins', 'throwing doggo coins', 'cs?', 'Minecraft'])

@bot.command
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('/Users/richardbann/Documents/GitHub/DoggoBot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print("commands loaded")


#Bank System

# @bot.command
# async def balance(ctx):
#     await open_account(ctx.author)
#
#     users = await get_bank_data()
#
#     wallet = users[str(user.id)]["wallet"] = 0
#     users[str(user.id)]["bank"] = 0
#
#     em = discord.Embed(title = f"{ctx.author.name}'s balance:", color=discord.Color.red())
#     em.add_field(name = "Wallet")

# async def open_account(user):
#
#     users = await get_bank_data()
#
#     if str(user.id) in users:
#          return False
#     else:
#         users[str(user.id)]["wallet"] = 0
#         users[str(user.id)]["bank"] = 0
#
#     with open("mainbank.json","r") as f:
#         json.dump(users, f)
#     return True
#
# async def get_bank_data():
#     with open("mainbank.json", "r") as f:
#         users = json.load(f)
#     return users












#BOT EVENTS

@bot.event
async def on_ready():
    change_status.start()
    #bot.remove_command("help")
    print('Bot is online.')


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server.')
    welcome_channel = bot.get_channel(833525136116154431)
    welc = ['just sheeeshed in :cold_face:',
            f"just crashed the party! Party\'s over everyone! :moyai:",
            'has joined the party! Always room for more bait :eyes:'
           ]
    print("Recognized that " + member.name + " joined")
    await welcome_channel.send(f"{member.mention} {random.choice(welc)}")

@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server.')
    welcome_channel = bot.get_channel(833525136116154431)
    print("Recognized that " + member.name + " left")
    left = ['has scrammed :person_in_manual_wheelchair:',
            'has left the server :ThinkNoose:',
            'just got quick deaded :dizzy_face:',
            'got deleted :wastebasket:'
            ]
    await welcome_channel.send(f"{member.mention} {random.choice(left)}")
    salut = ['So long, and thanks for all the fish.',
             'That\'s all folks!',
             '"Yabba Dabba Do!',
             'Mais um fraco saiu :ninja:',
             'And that\'s a wrap']
    await welcome_channel.send(f"\n{random.choice(salut)}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('This command doesn\'t exist. Use !help to see list of commands :ninja:')

# @bot.event
#sync def on_command_error(ctx, error):
 #   if isinstance(error, commands.MissingRequiredArgument):
 #       await ctx.send('Please pass in all required arguments.')

@bot.event
async def on_message(message):
    if message.content.find("cs?") != -1:
        await message.channel.send("<@" + str(340848834479390731) + ">")
        await message.channel.send("<@" + str(388397664229916684) + ">")
        await message.channel.send("<@" + str(285022682209058827) + ">")
        await message.channel.send("<@" + str(239453836513771531) + ">")
        await message.channel.send("<@" + str(339920949661007873) + ">")
        await message.channel.send("<@" + str(339925689027526656) + ">")

    if message.content.find("cs") != -1:
        if (re.search(r'\bcs\b', message.content, re.IGNORECASE)):
            await message.channel.send("<@" + str(340848834479390731) + ">")
            await message.channel.send("<@" + str(388397664229916684) + ">")
            await message.channel.send("<@" + str(285022682209058827) + ">")
            await message.channel.send("<@" + str(239453836513771531) + ">")
            await message.channel.send("<@" + str(339920949661007873) + ">")
            await message.channel.send("<@" + str(339925689027526656) + ">")

    if message.content.find("fortnite") != -1:
        if (re.search(r'\bfortnite\b', message.content, re.IGNORECASE)):
            await message.channel.send("<@" + str(239453836513771531) + ">")
            await message.channel.send("<@" + str(388397664229916684) + ">")
            await message.channel.send("<@" + str(285022682209058827) + ">")
            await message.channel.send("builda builda")

    if message.content.find("do") != 1:
        if (re.search(r'\bdo\b', message.content, re.IGNORECASE)):
            print("hi")
            randint = random.randint(1, 2)
            if randint == 1:
                if not message.author.bot:
                    phrase = re.split("do", message.content, maxsplit=1, flags=re.IGNORECASE)
                    print(phrase)
                    def is_empty(msg):
                        return re.search("^\s*$", msg)
                    empty = all([is_empty(string) for string in phrase])
                    if empty:
                        await message.channel.send(f'{message.author.mention}\'s mom has been done.')
                    if not empty:
                       if len(phrase) == 1:
                           print("one")
                           await message.channel.send(f'{phrase[0]}\'s mom has been done.')
                       if len(phrase) == 2:
                           print("two")
                           await message.channel.send(f'{phrase[1]}\'s mom has been done.')

    me = ["i", 'im', 'i\'m', 'mine', 'my']

    if message.content.find('i') != 1:
        if (re.search(r'\bi\b', message.content, re.IGNORECASE)):
            print("hi")
            randint = random.randint(1, 2)
            if randint == 1:
                if not message.author.bot:
                    await message.channel.send("When did I ask?")

    if message.content.find('im') != 1:
        if (re.search(r'\bim\b', message.content, re.IGNORECASE)):
            print("hi")
            randint = random.randint(1, 2)
            if randint == 1:
                if not message.author.bot:
                    await message.channel.send("When did I ask?")

    if message.content.find('i\'m') != 1:
        if (re.search(r'\bi\'m\b', message.content, re.IGNORECASE)):
            print("hi")
            randint = random.randint(1, 2)
            if randint == 1:
                if not message.author.bot:
                    await message.channel.send("When did I ask?")

    if message.content.find('mine') != 1:
        if (re.search(r'\bmine\b', message.content, re.IGNORECASE)):
            print("hi")
            randint = random.randint(1, 2)
            if randint == 1:
                if not message.author.bot:
                    await message.channel.send("When did I ask?")

    if message.content.find('my') != 1:
        if (re.search(r'\bmy\b', message.content, re.IGNORECASE)):
            print("hi")
            randint = random.randint(1, 2)
            if randint == 1:
                if not message.author.bot:
                    await message.channel.send("When did I ask?")

    # This part triggering not a real command error
  #  elif message.content == "!ping":
 #       await message.channel.send(f'Pong! {round(bot.latency * 1000)}ms')

    await bot.process_commands(message)

@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


bot.run(token)
