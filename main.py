import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

con = sqlite3.connect('blacklist.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS blacklist (userid text)')
con.commit()


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
            if blacklisted(member):
                print(member.display_name)
                try:
                    await force_update_member(member)
                except discord.errors.Forbidden:
                    print("Missing permissions")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!banish'):
        await update_all_members_in_guild(message.guild)

    if message.content.startswith('!smite'):
        if message.author.guild_permissions.administrator:
            member1 = message.author.guild.get_member(message.mentions[0].id)
            cur.execute("INSERT INTO blacklist VALUES (?)", (member1.id,))
            con.commit()
            await force_update_member(member1)


@client.event
async def on_member_update(before: discord.Member, after: discord.Member):

    if after.display_name[0] == '☹':
        return
    if blacklisted(after):
        await force_update_member(after)
    else:
        await update_member(after)


async def update_member(member: discord.Member):
    new_nick = member.display_name
    my_list = list(new_nick)

    if my_list[0] < '0' or '9' < my_list[0] < 'A':
        my_list[0] = '☹'

        new_nick = "".join(my_list)
        await member.edit(nick=new_nick)


async def force_update_member(member: discord.Member):

    new_nick = member.display_name
    my_list = list(new_nick)
    my_list[0] = '☹'

    new_nick = "".join(my_list)

    await member.edit(nick=new_nick)


def blacklisted(member: discord.Member):
    cur.execute("SELECT EXISTS(SELECT 1 FROM blacklist WHERE userid=?)", (member.id,))

    if cur.fetchone()[0]:
        return True
    return False


client.run(os.getenv('TOKEN'))
