import discord
import requests
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reminder_loop.start()

    def cog_unload(self):
        self.reminder_loop.cancel() 
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ addReminder.py is ready.")

    @tasks.loop(minutes=5) 
    async def reminder_loop(self):
        url = "https://habitude-habit-tracker.vercel.app/today/"
        token = os.getenv('BEARER_TOKEN')
        channel_id = int(os.getenv('REMINDER_CHANNEL_ID'))
        user_id = os.getenv('USER_ID')

        if token is None or channel_id is None or user_id is None:
            print("❌ Missing environment variables: BEARER_TOKEN, REMINDER_CHANNEL_ID, or USER_ID")
            return

        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                tasks = data.get('tasks', [])

                pending_tasks = [task for task in tasks if task.get('status', '').lower() == "pending"]

                if pending_tasks:  
                    channel = self.client.get_channel(channel_id)
                    if channel:
                        mention = f"<@{user_id}>" 
                        
                    
                        await channel.send(f"{mention} ⏳ You have pending tasks! Don't forget to complete them!")

                 
                        embed = discord.Embed(
                            title="⏳ Pending Task Reminder!",
                            color=discord.Color.orange()
                        )

                        for task in pending_tasks:
                            task_number = task.get('task_number', 'N/A')
                            name = task.get('name', 'No Name')

                            embed.add_field(
                                name=f"{task_number}. {name} ⏳",
                                value=f"**Status:** Pending",
                                inline=False
                            )

                        embed.set_footer(text="Stay productive! 💪")
                        await channel.send(embed=embed)

            else:
                print(f"❌ API request failed with status code {response.status_code}")

        except Exception as e:
            print(f"⚠️ Error in reminder loop: {e}")

async def setup(client):
    await client.add_cog(Reminder(client))
