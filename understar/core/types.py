
import discord
from discord import app_commands
from typing import Optional, Any
import os
import json
from .utils import get_logger

class DataManager:
    def __init__(self, plugin_name: str):
        self.plugin_name = plugin_name
        self.storage_path = os.path.join("data", "storage", plugin_name)
        os.makedirs(self.storage_path, exist_ok=True)
        self.logger = get_logger(f"Data-{plugin_name}")

    def _get_path(self, scope: str, id: Optional[int] = None) -> str:
        filename = f"{scope}.json"
        if id:
            filename = f"{scope}_{id}.json"
        return os.path.join(self.storage_path, filename)

    def get(self, scope: str, id: Optional[int] = None, default: Any = None) -> Any:
        path = self._get_path(scope, id)
        if not os.path.exists(path):
            return default if default is not None else {}
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load data for {scope}:{id}: {e}")
            return default if default is not None else {}

    def save(self, data: Any, scope: str, id: Optional[int] = None):
        path = self._get_path(scope, id)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.logger.error(f"Failed to save data for {scope}:{id}: {e}")

class FileManager:
    def __init__(self, plugin_name: str, asset_path: str = None):
        self.plugin_name = plugin_name
        self.storage = os.path.join("data", "storage", plugin_name)
        # Verify if asset_path is provided, else fallback to standard logic (though logic is now handled in PluginManager)
        self.assets = asset_path if asset_path else os.path.join("plugins", plugin_name, "assets")

class Plugin:
    def __init__(self, bot: discord.Client, tree: app_commands.CommandTree, asset_path: str = None):
        self.bot = bot
        self.tree = tree
        self.name = self.__class__.__name__
        self.logger = get_logger(self.name)
        self.data = DataManager(self.name)
        self.files = FileManager(self.name, asset_path)

    def on_load(self):
        pass

    def on_enable(self):
        pass

    def on_disable(self):
        pass

    def on_unload(self):
        pass


from discord.ext import tasks

# Decorators
def slash_command(name: str, description: str, dm_permission: bool = False, **kwargs):
    def decorator(func):
        # We attach metadata to the function to be processed by the loader
        func._is_slash_command = True
        func._command_name = name
        func._command_description = description
        func._dm_permission = dm_permission
        func._command_kwargs = kwargs
        return func
    return decorator

def listen(event_name):
    def decorator(func):
        func._is_listener = True
        func._infos = {"event_name": event_name}
        return func
    return decorator

def task(**kwargs):
    """
    Decorator to create a scheduled task.
    Wraps discord.ext.tasks.loop.
    Usage: @task(minutes=5)
    """
    def decorator(func):
        # Create the loop object immediately but don't start it
        # The PluginManager will handle starting it
        loop_obj = tasks.loop(**kwargs)(func)
        loop_obj._is_task = True
        return loop_obj
    return decorator
