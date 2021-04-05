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
    for guild in client.guilds:
        await update_all_members_in_guild(guild)


async def update_all_members_in_guild(guild: discord.Guild):
    members = guild.members
    for member in members:
        if not member.guild_permissions.administrator:
            await update_member(member)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!banish'):
        await update_all_members_in_guild(message.guild)


@client.event
async def on_member_update(before: discord.Member, after: discord.Member):

    await update_member(after)


async def update_member(member: discord.Member):

    new_nick = member.display_name
    my_list = list(new_nick)

    if my_list[0] < '0' or '9' < my_list[0] < 'A':
        my_list[0] = '☹'

        new_nick = "".join(my_list)
        await member.edit(nick=new_nick)

client.run(os.getenv('TOKEN'))
