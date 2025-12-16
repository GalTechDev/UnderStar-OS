
import discord
from discord import app_commands
from understar.core.plugin import Plugin, slash_command, listen, task
from understar.core.events import Event
from understar.core.permissions import Role, check_permission

class TemplatePlugin(Plugin):
    """
    Template Plugin for UnderStar-OS.
    Place this folder in your 'plugins/' directory.
    """

    def on_load(self):
        self.logger.info("Template Plugin Loaded!")

    @slash_command(name="hello", description="Say hello", dm_permission=True)
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")

    @task(minutes=10)
    async def loop_task(self):
        self.logger.info("Background task running...")
