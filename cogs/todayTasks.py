import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print("✅ todayTasks is ready.")

    @commands.command()
    async def today(self, ctx):
        url = "https://habitude-habit-tracker.vercel.app/today/"
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
                data = response.json() 
                tasks = data.get('tasks', [])

                if tasks:
                    embed = discord.Embed(
                        title="✅ Today's Tasks",
                        description="Here are your tasks for today:",
                        color=discord.Color.blue()
                    )

                    for task in tasks:
                        task_number = task.get('task_number', 'N/A')
                        name = task.get('name', 'No Name')
                        status = task.get('status', 'No Status')

                        emoji = "✅" if status.lower() == "completed" else "⏳"

                        embed.add_field(
                            name=f"{task_number}. {name}  {emoji}",
                            value=f"**Status:** {status}",
                            inline=False
                        )

                    embed.set_footer(text="Habitude - Stay on track! 📌")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("🎉 No tasks for today!")

            else:
                await ctx.send("❌ **Error:** Failed to retrieve data from the API.")

        except Exception as e:
            await ctx.send(f"⚠️ **An error occurred:** `{e}`")

async def setup(client):
    await client.add_cog(Test(client))
