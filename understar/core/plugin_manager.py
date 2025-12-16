
import os
import importlib.util
import inspect
from typing import Dict, Any
from .utils import get_logger
from .types import Plugin
from .events import Event

class PluginManager:
    def __init__(self, kernel):
        self.kernel = kernel
        self.logger = get_logger("PluginManager")
        self.plugins: Dict[str, Plugin] = {}
        # System plugins (internal)
        self.system_plugins_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")
        # User plugins (cwd)
        self.user_plugins_dir = os.path.join(os.getcwd(), "plugins")

    async def load_all_plugins(self):
        self.logger.info("Loading plugins...")
        
        # Load System Plugins
        if os.path.exists(self.system_plugins_dir):
            for item in os.listdir(self.system_plugins_dir):
                if os.path.isdir(os.path.join(self.system_plugins_dir, item)):
                     await self.load_plugin(item, is_system=True)

        # Load User Plugins
        if os.path.exists(self.user_plugins_dir):
            for item in os.listdir(self.user_plugins_dir):
                if os.path.isdir(os.path.join(self.user_plugins_dir, item)):
                     await self.load_plugin(item, is_system=False)

    async def load_plugin(self, plugin_name: str) -> bool:
        try:
            # Import module dynamicallly
            module_name = f"understar.plugins.{plugin_name}"
            
            # Check if already loaded
            if plugin_name in self.plugins:
                self.logger.info(f"Plugin {plugin_name} already loaded.")
                return True

            spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.plugins_dir, plugin_name, "__init__.py"))
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load spec for {plugin_name}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find Plugin class
            plugin_class = None
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Plugin) and obj is not Plugin:
                    plugin_class = obj
                    break
            
            if not plugin_class:
                self.logger.warning(f"No Plugin class found in {plugin_name}")
                return False

            # Instantiate Plugin
            # Determine asset path
            asset_path = os.path.join(path, "assets")
            plugin_instance = plugin_class(self.kernel.client, self.kernel.tree, asset_path=asset_path)
            
            # Inject DataManager and FileManager (already done in Plugin.__init__ but ensures connection)
            # Register Listeners
            self._register_listeners(plugin_instance)
            
            # Register Slash Commands
            self._register_commands(plugin_instance)

            # Register and Start Tasks
            self._register_tasks(plugin_instance)

            # Verification: Check permissions
            # TODO: Check if plugin is strictly enabled for this guild (at runtime/event time)

            # Call on_load
            if inspect.iscoroutinefunction(plugin_instance.on_load):
                await plugin_instance.on_load()
            else:
                plugin_instance.on_load()
            
            self.plugins[plugin_name] = plugin_instance
            self.logger.info(f"Plugin Loaded: {plugin_name}")
            
            # Notify Event Bus
            await self.kernel.bus.emit(Event.ON_PLUGIN_LOAD, plugin_name)
            
            return True

        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_name}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _register_listeners(self, plugin_instance: Plugin):
        for name, method in inspect.getmembers(plugin_instance):
            if hasattr(method, "_is_listener"):
                event_name = method._infos["event_name"]
                self.kernel.bus.subscribe(event_name, method)

    def _register_commands(self, plugin_instance: Plugin):
        for name, method in inspect.getmembers(plugin_instance):
            if hasattr(method, "_is_slash_command"):
                # Register to CommandTree
                command_name = method._command_name
                description = method._command_description
                dm_permission = method._dm_permission
                kwargs = method._command_kwargs
                
                # We need to wrap the method to handle 'self' if it's not bound correctly by app_commands
                # app_commands.command automatically handles binding if defined inside a class inheriting from specific discord types
                # But here Plugin inherits from object.
                # However, we are adding it to the tree manually? 
                # No, standard way is creating a Command object or using the decorator on a Group.
                # For simplicity in V2, we might attach to the global tree.
                
                command = discord.app_commands.Command(
                    name=command_name,
                    description=description,
                    callback=method, # The method is bound to the instance
                    dm_permission=dm_permission,
                    **kwargs
                )
                
                # Add check to enforce guild configuration
                async def interaction_check(interaction: discord.Interaction) -> bool:
                    return await self._check_plugin_enabled(plugin_instance.name, interaction.guild_id)
                
                command.add_check(interaction_check)
                
                self.kernel.tree.add_command(command)
                self.logger.debug(f"Registered command /{command_name} for {plugin_instance.name}")

    async def _check_plugin_enabled(self, plugin_name: str, guild_id: int) -> bool:
        if not guild_id: return True # DM always enabled (or handled by dm_permission)
        if plugin_name == "config": return True # Config always enabled
        
        # We need to access Config plugin data. 
        # Since DataManager is standardized, we can read the file directly or use a helper.
        # Ideally, we should ask the Config plugin instance, but here we can just use DataManager logic 
        # as it is stateless file access basically.
        try:
            from .types import DataManager
            data = DataManager("config")
            config = data.get(scope="guild", id=guild_id, default={})
            disabled = config.get("disabled_apps", [])
            return plugin_name not in disabled
        except Exception:
            return True # Fail safe enabled

    def _register_tasks(self, plugin_instance: Plugin):
        for name, obj in inspect.getmembers(plugin_instance):
            if hasattr(obj, "_is_task"):
                try:
                    obj.start()
                    self.logger.debug(f"Started task {name} for {plugin_instance.name}")
                except Exception as e:
                    self.logger.error(f"Failed to start task {name}: {e}")

    async def unload_plugin(self, plugin_name: str):
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            # Call on_unload
            if inspect.iscoroutinefunction(plugin.on_unload):
                await plugin.on_unload()
            else:
                plugin.on_unload()
            
            # Stop tasks
            for name, obj in inspect.getmembers(plugin):
                if hasattr(obj, "_is_task"):
                    obj.cancel()
            
            # Remove from dict
            del self.plugins[plugin_name]
            # TODO: Remove listeners and commands (complex with discord.py's Tree)
            self.logger.info(f"Plugin Unloaded: {plugin_name}")
