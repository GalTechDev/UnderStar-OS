
from enum import Enum

class Event(Enum):
    # Discord Events
    ON_READY = "on_ready"
    ON_MESSAGE = "on_message"
    ON_MESSAGE_EDIT = "on_message_edit"
    ON_MESSAGE_DELETE = "on_message_delete"
    ON_MEMBER_JOIN = "on_member_join"
    ON_MEMBER_REMOVE = "on_member_remove"
    ON_GUILD_JOIN = "on_guild_join"
    ON_GUILD_REMOVE = "on_guild_remove"
    ON_REACTION_ADD = "on_reaction_add"
    ON_REACTION_REMOVE = "on_reaction_remove"
    
    # Internal Events
    ON_PLUGIN_LOAD = "on_plugin_load"
    ON_PLUGIN_UNLOAD = "on_plugin_unload"
