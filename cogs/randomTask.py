import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class RandomTask(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ randomTask.py is ready.")

    @commands.command(
        name="random_task", 
        aliases=["rt", "random", "quicktask"]
    )
    async def random_task(self, ctx):
        url = "https://habitude-habit-tracker.vercel.app/random_task/"
        token = os.getenv('BEARER_TOKEN')

        if token is None:
            await ctx.send("❌ **Error:** BEARER_TOKEN is missing in the environment variables.")
            return

        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                task = response.json() 

                task_name = task.get('name', 'No Task Available')

                embed = discord.Embed(
                    title="🎲 Random Task",
                    description=f"**{task_name}**",
                    color=discord.Color.blue()
                )

                embed.set_footer(text="Habitude - Stay on track! 🔄")

                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ **Error:** Failed to retrieve a random task.")

        except Exception as e:
            await ctx.send(f"⚠️ **An error occurred:** `{e}`")

async def setup(client):
    await client.add_cog(RandomTask(client))
