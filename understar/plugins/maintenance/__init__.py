
import discord
from core.plugin import Plugin, slash_command, listen
from core.events import Event
from core.permissions import Role, check_permission

class MaintenancePlugin(Plugin):
    @listen(Event.ON_READY)
    async def on_ready(self):
        self.logger.info("Maintenance Plugin: Bot is ready!")

    @slash_command(name="ping", description="Check bot latency", dm_permission=True)
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! used {latency}ms")

    @slash_command(name="clear", description="Clear messages", dm_permission=False)
    @check_permission(Role.GUILD_MANAGER)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Deleted {len(deleted)} messages.", ephemeral=True)
