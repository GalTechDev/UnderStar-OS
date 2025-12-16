
import asyncio
from typing import Callable, Dict, List, Any
from .utils import get_logger
from .events import Event

class EventBus:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.logger = get_logger("EventBus")

    def subscribe(self, event_name: Any, callback: Callable):
        # Support both Enum and string (though Enum is preferred)
        key = event_name.value if isinstance(event_name, Event) else event_name
        
        if key not in self.listeners:
            self.listeners[key] = []
        self.listeners[key].append(callback)
        self.logger.debug(f"Subscribed {callback.__name__} to {key}")

    async def emit(self, event_name: Any, *args, **kwargs):
        key = event_name.value if isinstance(event_name, Event) else event_name
        
        if key in self.listeners:
            # Execute all listeners currently
            # In V3 we might want priority support
            listeners = self.listeners[key]
            if not listeners:
                return

            tasks = []
            for listener in listeners:
                try:
                    # Check plugin enabled
                    plugin_instance = getattr(listener, "__self__", None)
                    if plugin_instance and hasattr(plugin_instance, "name"):
                         guild_id = None
                         for arg in args:
                             if hasattr(arg, "guild") and arg.guild:
                                 guild_id = arg.guild.id
                                 break
                             if hasattr(arg, "guild_id") and arg.guild_id:
                                 guild_id = arg.guild_id
                                 break
                         
                         if guild_id:
                             from .types import DataManager
                             data = DataManager("config")
                             config = data.get(scope="guild", id=guild_id, default={})
                             if plugin_instance.name in config.get("disabled_apps", []):
                                 continue

                    # Check if coroutine
                    if asyncio.iscoroutinefunction(listener):
                        tasks.append(listener(*args, **kwargs))
                    else:
                        listener(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"Error in listener {listener.__name__} for event {key}: {e}")
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
