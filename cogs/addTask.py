import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class AddTask(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ addTask.py is ready.")

    @commands.command(
        name="add_task",
        aliases=["new_task", "task_add"]
    )
    async def add_task(self, ctx, *, task_name: str):
        url = "https://habitude-habit-tracker.vercel.app/add_task/"
        token = os.getenv('BEARER_TOKEN')

        if not token:
            await ctx.send("❌ **Error:** BEARER_TOKEN is missing in the environment variables.")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        data = {
            "name": task_name
        }
        try:
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 201:
                embed = discord.Embed(
                    title="✅ Task Added",
                    description=f"The task **'{task_name}'** has been successfully added.",
                    color=discord.Color.green()
                )
                embed.set_footer(text="Habitude - Keep up the good work! 🎯")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ **Error:** Failed to add task. (Status Code: {response.status_code})")

        except requests.exceptions.RequestException as e:
            await ctx.send(f"⚠️ **Request Error:** {e}")
        except Exception as e:
            await ctx.send(f"⚠️ **An error occurred:** {e}")

async def setup(client):
    await client.add_cog(AddTask(client))
