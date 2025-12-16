
import discord
from discord.ext import commands
from typing import Optional
from .event_bus import EventBus
from .plugin_manager import PluginManager
from .permissions import PermissionManager
from .utils import get_logger, setup_logging
from .events import Event

class Kernel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Kernel, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
        
        setup_logging()
        self.logger = get_logger("Kernel")
        
        # Initialize Components
        self.bus = EventBus()
        self.permissions = PermissionManager()
        
        # Discord Client setup
        intents = discord.Intents.all()
        self.client = discord.Client(intents=intents)
        self.tree = discord.app_commands.CommandTree(self.client)
        
        self.plugin_manager = PluginManager(self)
        
        self.initialized = True

    async def start(self, token: str):
        self.logger.info("Starting UnderStar-OS V2 Kernel...")
        
        # Register core events
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.client.event(self.on_interaction)
        
        # Load Plugins
        await self.plugin_manager.load_all_plugins()
        
        await self.client.start(token)

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.client.user} (ID: {self.client.user.id})")
        await self.bus.emit(Event.ON_READY)
        
        # Sync Commands (Global for now, can be guild specific in Config plugin)
        # await self.tree.sync()
        self.logger.info("Commands synced.")

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        await self.bus.emit(Event.ON_MESSAGE, message)

    async def on_interaction(self, interaction: discord.Interaction):
        # We don't need to manually emit interaction events for slash commands
        # as CommandTree handles them, but we might want a generic hook
        await self.bus.emit("on_interaction", interaction)

kernel = Kernel()
