
from enum import Enum, auto
import discord
from discord import app_commands
import os
from .utils import get_logger

class Role(Enum):
    BOT_ADMIN = auto()
    GUILD_MANAGER = auto()
    USER = auto()

class PermissionManager:
    def __init__(self):
        self.logger = get_logger("Permissions")
        self.admin_ids = []
        self._load_admins()

    def _load_admins(self):
        # Load from .env or config file
        # For V2, we'll try to load from a simple json config in data/
        try:
            # Placeholder for config loading
            pass
        except Exception as e:
            self.logger.error(f"Failed to load admins: {e}")

    def check(self, interaction: discord.Interaction, required_role: Role) -> bool:
        if required_role == Role.USER:
            return True
        
        if required_role == Role.BOT_ADMIN:
            return interaction.user.id in self.admin_ids
        
        if required_role == Role.GUILD_MANAGER:
            # Check if user has global admin
            if interaction.user.id in self.admin_ids:
                return True
            # Check if user has 'Manage Server' permission or specific role
            # Todo: Integrate with Config Plugin for custom role mapping
            if interaction.permissions.manage_guild:
                return True
                
        return False

# Decorator
def check_permission(role: Role):
    def decorator(func):
        func._required_permission = role
        return func
    return decorator
