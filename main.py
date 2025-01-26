import os
import discord
from discord.ext import commands,tasks
import asyncio
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('BOT_TOKEN')


client = commands.Bot(command_prefix="h!", intents=discord.Intents.all()) 

client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("h!help"))
    print("Success : Bot is connected to Discord")

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            # print(f"{filename[:-3]} is loaded.")

async def main():
    async with client:
        await load()
        await client.start(token)

asyncio.run(main())