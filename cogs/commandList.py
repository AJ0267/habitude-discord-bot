import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ commandList.py is ready.")

    @commands.command(
        name="help",
        aliases=["h", "commands"]
    )
    async def help(self, ctx):
        help_embed = discord.Embed(
            title="Habitude Bot Commands",
            description="All available commands for the Habitude bot.",
            color=discord.Color.blue()
        )

        help_embed.add_field(
            name="Habitude Specific Commands",
            value="`h!today` - Get today's tasks\n"
                  "`h!add_task [task name]` - Add a new task\n"
                  "`h!completed [task_id]` - Mark a task as completed\n"
                  "`h!delete_task [task_id]` - Delete a task\n"
                  "`h!random_task` - Get a random task\n",
            inline=False
        )

        help_embed.set_footer(text="Use 'h!command_name' to execute a command.")
        await ctx.send(embed=help_embed)

async def setup(client):
    await client.add_cog(HelpCommand(client))
