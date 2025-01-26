import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class CompleteTask(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ taskCompletion.py is ready.")

    @commands.command(
        name="completed",
        aliases=["done", "finish", "mark"]
    )
    async def completed(self, ctx, task_number):
        url = f"https://habitude-habit-tracker.vercel.app/completed/{task_number}/"
        token = os.getenv('BEARER_TOKEN')

        if token is None:
            await ctx.send("❌ **Error:** BEARER_TOKEN is missing in the environment variables.")
            return

        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:
            response = requests.post(url, headers=headers)

            if response.status_code == 200:
                embed = discord.Embed(
                    title="✅ Task Completed",
                    description=f"Task `{task_number}` has been marked as **completed**.",
                    color=discord.Color.green()
                )
                embed.set_footer(text="Habitude - Keep up the good work! 🎯")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ **Error:** Failed to mark task `{task_number}` as completed. (Status Code: {response.status_code})")

        except Exception as e:
            await ctx.send(f"⚠️ **An error occurred:** `{e}`")

async def setup(client):
    await client.add_cog(CompleteTask(client))
