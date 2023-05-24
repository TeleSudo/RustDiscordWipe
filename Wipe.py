import discord
from discord.ext import commands
import datetime
import asyncio

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

WIPE_INTERVAL_DAYS = 1 #put wipe day here 
next_wipe = datetime.datetime.now() + datetime.timedelta(days=WIPE_INTERVAL_DAYS)

async def get_wipe_channel():
    guild = client.get_guild()  #put channel id in guild
    channel = guild.get_channel() #put channel id in guild
    return channel

async def send_wipe_message():
    channel = await get_wipe_channel()
    time_left = next_wipe - datetime.datetime.now()
    days_left = time_left.days
    hours_left = time_left.seconds // 3600
    minutes_left = (time_left.seconds // 60) % 60
    embed = discord.Embed(title="IranRust [2x] Server Wipe Counter", color=0x00ff00) #server name 
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/996016412055318628/996123444641013780/Untitled-1.png") #your logo
    embed.add_field(name="Days Left", value=f"{days_left} days", inline=True)
    embed.add_field(name="Hours Left", value=f"{hours_left} hours", inline=True)
    embed.add_field(name="Minutes Left", value=f"{minutes_left} minutes", inline=True)
    message = await channel.send(embed=embed)
    return message

async def update_wipe_message():
    global next_wipe
    while True:
        if next_wipe < datetime.datetime.now():
            next_wipe = datetime.datetime.now() + datetime.timedelta(days=WIPE_INTERVAL_DAYS)
        channel = await get_wipe_channel()
        message = await send_wipe_message()
        time_left = next_wipe - datetime.datetime.now()
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        minutes_left = (time_left.seconds // 60) % 60
        embed = discord.Embed(title="IranRust [2x] Server Wipe Counter", color=0x00ff00) #server name 
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/996016412055318628/996123444641013780/Untitled-1.png") #your logo
        embed.add_field(name="Days Left", value=f"{days_left} days", inline=True)
        embed.add_field(name="Hours Left", value=f"{hours_left} hours", inline=True)
        embed.add_field(name="Minutes Left", value=f"{minutes_left} minutes", inline=True)
        await message.edit(embed=embed)
        await asyncio.sleep(60)

async def update_status():
    global next_wipe
    while True:
        if next_wipe < datetime.datetime.now():
            next_wipe = datetime.datetime.now() + datetime.timedelta(days=WIPE_INTERVAL_DAYS)
        time_left = next_wipe - datetime.datetime.now()
        days_left = time_left.days
        hours_left = time_left.seconds // 3600
        minutes_left = (time_left.seconds // 60) % 60
        await client.change_presence(activity=discord.Game(f'Next wipe in {days_left} days and {hours_left} hours and {minutes_left} minutes left.'))
        await asyncio.sleep(10)

async def main():
    await client.wait_until_ready()
    client.loop.create_task(update_wipe_message())
    client.loop.create_task(update_status())

    
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Update the bot's status every 10 seconds
    client.loop.create_task(update_status())
    print('Status updated')
    # Update the wipe message every minute
    client.loop.create_task(update_wipe_message())
    print('Wipe message updated')



client.run('') #put your discord token
