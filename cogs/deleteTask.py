import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class DeleteTask(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ deleteTask.py is ready.")

    @commands.command(
        name="delete_task",
        aliases=["remove_task", "task_delete"]
    )
    async def delete_task(self, ctx, task_id):
        url = f"https://habitude-habit-tracker.vercel.app/delete_task/{task_id}/"
        token = os.getenv('BEARER_TOKEN')

        if not token:
            await ctx.send("❌ **Error:** BEARER_TOKEN is missing in the environment variables.")
            return

        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:
            response = requests.delete(url, headers=headers)

            if response.status_code == 200:
                embed = discord.Embed(
                    title="✅ Task Deleted",
                    description=f"Task `{task_id}` has been successfully deleted.",
                    color=discord.Color.green()
                )
                embed.set_footer(text="Habitude - Stay productive!")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ **Error:** Failed to delete task `{task_id}`. (Status Code: {response.status_code})")

        except requests.exceptions.RequestException as e:
            await ctx.send(f"⚠️ **Request Error:** {e}")
        except Exception as e:
            await ctx.send(f"⚠️ **An error occurred:** {e}")

async def setup(client):
    await client.add_cog(DeleteTask(client))
