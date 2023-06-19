import discord

class Event:
    """"""
    def __init__(self) -> None:
        self.on_raw_app_command_permissions_update = self.on_raw_app_command_permissions_update
        self.on_app_command_completion = self.on_app_command_completion
        self.on_app_command_error = self.on_app_command_error
        self.on_automod_rule_create = self.on_automod_rule_create
        self.on_automod_rule_update = self.on_automod_rule_update
        self.on_automod_rule_delete = self.on_automod_rule_delete
        self.on_automod_action = self.on_automod_action
        self.on_guild_channel_delete = self.on_guild_channel_delete
        self.on_guild_channel_create = self.on_guild_channel_create
        self.on_guild_channel_update = self.on_guild_channel_update
        self.on_guild_channel_pins_update = self.on_guild_channel_pins_update
        self.on_private_channel_update = self.on_private_channel_update
        self.on_private_channel_pins_update = self.on_private_channel_pins_update
        self.on_typing = self.on_typing
        self.on_raw_typing = self.on_raw_typing
        self.on_connect = self.on_connect
        self.on_disconnect = self.on_disconnect
        self.on_shard_connect = self.on_shard_connect
        self.on_shard_disconnect = self.on_shard_disconnect
        self.on_error = self.on_error
        self.on_socket_event_type = self.on_socket_event_type
        self.on_socket_raw_receive = self.on_socket_raw_receive
        self.on_socket_raw_send = self.on_socket_raw_send
        self.on_ready = self.on_ready
        self.on_resumed = self.on_resumed
        self.on_shard_ready = self.on_shard_ready
        self.on_shard_resumed = self.on_shard_resumed
        self.on_guild_available = self.on_guild_available
        self.on_guild_unavailable = self.on_guild_unavailable
        self.on_guild_join = self.on_guild_join
        self.on_guild_remove = self.on_guild_remove
        self.on_guild_update = self.on_guild_update
        self.on_guild_emojis_update = self.on_guild_emojis_update
        self.on_guild_stickers_update = self.on_guild_stickers_update
        self.on_invite_create = self.on_invite_create
        self.on_invite_delete = self.on_invite_delete
        self.on_integration_create = self.on_integration_create
        self.on_integration_update = self.on_integration_update
        self.on_guild_integrations_update = self.on_guild_integrations_update
        self.on_webhooks_update = self.on_webhooks_update
        self.on_raw_integration_delete = self.on_raw_integration_delete
        self.on_interaction = self.on_interaction
        self.on_member_join = self.on_member_join
        self.on_member_remove = self.on_member_remove
        self.on_raw_member_remove = self.on_raw_member_remove
        self.on_member_update = self.on_member_update
        self.on_user_update = self.on_user_update
        self.on_member_ban = self.on_member_ban
        self.on_member_unban = self.on_member_unban
        self.on_presence_update = self.on_presence_update
        self.on_message = self.on_message
        self.on_message_edit = self.on_message_edit
        self.on_message_delete = self.on_message_delete
        self.on_bulk_message_delete = self.on_bulk_message_delete
        self.on_raw_message_edit = self.on_raw_message_edit
        self.on_raw_message_delete = self.on_raw_message_delete
        self.on_raw_bulk_message_delete = self.on_raw_bulk_message_delete
        self.on_reaction_add = self.on_reaction_add
        self.on_reaction_remove = self.on_reaction_remove
        self.on_reaction_clear = self.on_reaction_clear
        self.on_reaction_clear_emoji = self.on_reaction_clear_emoji
        self.on_raw_reaction_add = self.on_raw_reaction_add
        self.on_raw_reaction_remove = self.on_raw_reaction_remove
        self.on_raw_reaction_clear = self.on_raw_reaction_clear
        self.on_raw_reaction_clear_emoji = self.on_raw_reaction_clear_emoji
        self.on_guild_role_create = self.on_guild_role_create
        self.on_guild_role_delete = self.on_guild_role_delete
        self.on_guild_role_update = self.on_guild_role_update
        self.on_scheduled_event_create = self.on_scheduled_event_create
        self.on_scheduled_event_delete = self.on_scheduled_event_delete
        self.on_scheduled_event_update = self.on_scheduled_event_update
        self.on_scheduled_event_user_add = self.on_scheduled_event_user_add
        self.on_scheduled_event_user_remove = self.on_scheduled_event_user_remove
        self.on_stage_instance_create = self.on_stage_instance_create
        self.on_stage_instance_delete = self.on_stage_instance_delete
        self.on_stage_instance_update = self.on_stage_instance_update
        self.on_thread_create = self.on_thread_create
        self.on_thread_join = self.on_thread_join
        self.on_thread_update = self.on_thread_update
        self.on_thread_remove = self.on_thread_remove
        self.on_thread_delete = self.on_thread_delete
        self.on_raw_thread_update = self.on_raw_thread_update
        self.on_raw_thread_delete = self.on_raw_thread_delete
        self.on_thread_member_join = self.on_thread_member_join
        self.on_thread_member_remove = self.on_thread_member_remove
        self.on_raw_thread_member_remove = self.on_raw_thread_member_remove
        self.on_voice_state_update = self.on_voice_state_update


    def event(self):
        def apply(funct):
            if funct.__name__ in self.__dict__.keys():
                self.__dict__[funct.__name__] = funct
                return funct
            else:
                raise Exception(f"Event : {funct.__name__} are unknow")
        return apply

    #App Commands

    async def on_raw_app_command_permissions_update(self, payload):
        pass

    async def on_app_command_completion(self, interaction, command):
        pass

    async def on_app_command_error(self, ctx: discord.Interaction, error: discord.app_commands.AppCommandError):
        pass

    #AutoMod

    async def on_automod_rule_create(self, rule):
        pass

    async def on_automod_rule_update(self, rule):
        pass

    async def on_automod_rule_delete(self, rule):
        pass

    async def on_automod_action(self, execution):
        pass

    #Channels

    async def on_guild_channel_delete(self, channel):
        pass

    async def on_guild_channel_create(self, channel):
        pass

    async def on_guild_channel_update(self, before, after):
        pass

    async def on_guild_channel_pins_update(self, channel, last_pin):
        pass

    async def on_private_channel_update(self, before, after):
        pass

    async def on_private_channel_pins_update(self, channel, last_pin):
        pass

    async def on_typing(self, channel, user, when):
        pass

    async def on_raw_typing(self, payload):
        pass

    #Connection

    async def on_connect(self):
        pass

    async def on_disconnect(self):
        pass

    async def on_shard_connect(self, shard_id):
        pass

    async def on_shard_disconnect(self, shard_id):
        pass

    #Debug

    async def on_error(self, event, *args, **kwargs):
        pass

    async def on_socket_event_type(self, event_type):
        pass

    async def on_socket_raw_receive(self, msg):
        pass

    async def on_socket_raw_send(self, payload):
        pass

    #Gateway

    async def on_ready(self):
        pass

    async def on_resumed(self):
        pass

    async def on_shard_ready(self, shard_id):
        pass

    async def on_shard_resumed(self, shard_id):
        pass

    #Guilds

    async def on_guild_available(self, guild):
        pass

    async def on_guild_unavailable(self, guild):
        pass

    async def on_guild_join(self, guild):
        pass

    async def on_guild_remove(self, guild):
        pass

    async def on_guild_update(self, before, after):
        pass

    async def on_guild_emojis_update(self, guild, before, after):
        pass

    async def on_guild_stickers_update(self, guild, before, after):
        pass

    async def on_invite_create(self, invite):
        pass

    async def on_invite_delete(self, invite):
        pass

    #Integrations

    async def on_integration_create(self, integration):
        pass

    async def on_integration_update(self, integration):
        pass

    async def on_guild_integrations_update(self, guild):
        pass

    async def on_webhooks_update(self, channel):
        pass

    async def on_raw_integration_delete(self, payload):
        pass

    #Interactions

    async def on_interaction(self, interaction):
        pass

    #Members

    async def on_member_join(self, member):
        pass

    async def on_member_remove(self, member):
        pass

    async def on_raw_member_remove(self, payload):
        pass

    async def on_member_update(self, before, after):
        pass

    async def on_user_update(self, before, after):
        pass

    async def on_member_ban(self, guild, user):
        pass

    async def on_member_unban(self, guild, user):
        pass

    async def on_presence_update(self, before, after):
        pass

    #Messages

    async def on_message(self, message):
        pass

    async def on_message_edit(self, before, after):
        pass

    async def on_message_delete(self, message):
        pass

    async def on_bulk_message_delete(self, messages):
        pass

    async def on_raw_message_edit(self, payload):
        pass

    async def on_raw_message_delete(self, payload):
        pass

    async def on_raw_bulk_message_delete(self, payload):
        pass

    #Reactions

    async def on_reaction_add(self, reaction, user):
        pass

    async def on_reaction_remove(self, reaction, user):
        pass

    async def on_reaction_clear(self, message, reactions):
        pass

    async def on_reaction_clear_emoji(self, reaction):
        pass

    async def on_raw_reaction_add(self, payload):
        pass

    async def on_raw_reaction_remove(self, payload):
        pass

    async def on_raw_reaction_clear(self, payload):
        pass

    async def on_raw_reaction_clear_emoji(self, payload):
        pass

    #Roles

    async def on_guild_role_create(self, role):
        pass

    async def on_guild_role_delete(self, role):
        pass

    async def on_guild_role_update(self, before, after):
        pass

    #Scheduled Events

    async def on_scheduled_event_create(self, event):
        pass

    async def on_scheduled_event_delete(self, event):
        pass

    async def on_scheduled_event_update(self, before, after):
        pass

    async def on_scheduled_event_user_add(self, event, user):
        pass

    async def on_scheduled_event_user_remove(self, event, user):
        pass

    #Stages

    async def on_stage_instance_create(self, stage_instance):
        pass

    async def on_stage_instance_delete(self, stage_instance):
        pass

    async def on_stage_instance_update(self, before, after):
        pass

    #Threads

    async def on_thread_create(self, thread):
        pass

    async def on_thread_join(self, thread):
        pass

    async def on_thread_update(self, before, after):
        pass

    async def on_thread_remove(self, thread):
        pass

    async def on_thread_delete(self, thread):
        pass

    async def on_raw_thread_update(self, payload):
        pass

    async def on_raw_thread_delete(self, payload):
        pass

    async def on_thread_member_join(self, member):
        pass

    async def on_thread_member_remove(self, member):
        pass

    async def on_raw_thread_member_remove(self, payload):
        pass

    #Voice

    async def on_voice_state_update(self, member, before, after):
        pass
