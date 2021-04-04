import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)


# client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!banish'):
        # Scan every user and call on_member_update
        pass


@client.event
async def on_member_update(before: discord.Member, after: discord.Member):

    new_nick = after.nick
    my_list = list(new_nick)

    if my_list[0] <= '@':
        my_list[0] = '☹'

        new_nick = "".join(my_list)
        await after.edit(nick=new_nick)


client.run(os.getenv('TOKEN'))
