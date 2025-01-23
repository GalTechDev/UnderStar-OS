# coding: utf-8
from discord.ext import commands as discord_commands
from discord.ext import tasks as discord_tasks
from itertools import cycle
from pathlib import Path
import os
import discord
import time
import sys
from .system.lib import App, MISSING, BOT_VERSION, types, convert_time, import_module
from .system import app as sys_app
import asyncio
import json
import logging
from logging import info, warning, error

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level = logging.INFO)

DOWNLOAD_FOLDER: str = "download"
SYS_FOLDER: str = "system"
TOKEN_FOLDER: str = "token"
SAVE_FOLDER: str = "save"
SAVE_APP_FOLDER: str = os.path.join("save", "app") 
SAVE_SYS_FOLDER: str = os.path.join("save", "system")
APP_FOLDER: str = "app"
BOT_TOKEN_PATH: str = os.path.join(f"{TOKEN_FOLDER}", "bot_token")
UPDATE_FILE: str = os.path.join(f"{SYS_FOLDER}","app", "update", "update.pyw")
GUILD_FILE: str = os.path.join(f"{SAVE_FOLDER}", f"{SYS_FOLDER}", "guilds.json")

programmer = os.path.basename(sys.argv[0])


class OS:
    Lib = App()

    vals: list = [DOWNLOAD_FOLDER, TOKEN_FOLDER, SAVE_FOLDER, SAVE_APP_FOLDER, APP_FOLDER, SAVE_SYS_FOLDER]

    for name in vals:
        Path(name).mkdir(exist_ok=True)

    files: list = ["guilds.json", "app_store.json"]

    for file in files:
        if not file in os.listdir(SAVE_SYS_FOLDER):
            with open(os.path.join(SAVE_SYS_FOLDER, file), "w", encoding="utf8") as f:
                pass

        try:
            with open(os.path.join(SAVE_SYS_FOLDER, file), "r", encoding="utf8") as f:
                json.loads(f.read())

        except json.JSONDecodeError:
            with open(os.path.join(SAVE_SYS_FOLDER, file), "w", encoding="utf8") as f:
                f.write(json.dumps({} if file == "guilds.json" else {"rolemanager": "https://github.com/GalTechDev/rolemanager/archive/refs/heads/main.zip", "uno": "https://github.com/GalTechDev/uno/archive/refs/heads/main.zip", "welcome": "https://github.com/GalTechDev/welcome/archive/refs/heads/main.zip"}))

    BOT_TOKEN: str = ""

    intents = discord.Intents.all()

    timer = time.time()

    def start(self):
        self.client.run(self.BOT_TOKEN)

    async def import_apps(self, sys: bool = False) -> None:
        """"""
        #print((self.all_app.items() if not sys else sys_app.all_app.items()))

        for app_name, app in (self.all_app.items() if not sys else sys_app.all_app.items()):
            info(f" * IMPORT {app_name}: ")

            app.Lib.init(self.client, discord_tasks, self.all_app)
            app.Lib.set_app_name(app_name)

            if not os.path.exists(os.path.join(app.Lib.save.save_path, app_name)):
                os.mkdir(os.path.join(app.Lib.save.save_path, app_name))

            # Task

            loaded: int = 0
            errors: int = 0
            error_lst: list = []
            ttasks: list = []

            try:
                for task in app.Lib.app.all_tasks:
                    try:
                        ttasks.append(discord_tasks.Loop[discord_tasks.LF](coro=task.function, seconds=task.seconds, minutes=task.minutes, hours=task.hours, count=task.count, time=task.time, reconnect=task.reconnect))
                        #terminal(callback=task.function, aliases=[f"{app_name}-{task.function.__name__}"])

                    except Exception as error:
                        errors += 1
                        error_lst.append(error)

                for task in ttasks:
                    try:
                        asyncio.gather(task._loop())
                        loaded += 1

                    except Exception as error:
                        errors += 1
                        error_lst.append(error)

            except Exception as error:
                error(error)

            info(f" * - Task : {loaded} loaded | {errors} error : {error_lst}")

            # Command & Slash
            if len(self.Lib.store.get_guilds_installed(app_name)) > 0 or sys:

                # Command
                loaded: int = 0
                errors: int = 0
                error_lst: list = []

                for command in app.Lib.app.commands:
                    try:
                        new_com = discord_commands.Command(command.command,name=f"{app_name}-{command.name}" if not command.force_name else command.name,help=command.help,aliases=command.aliases,checks=command.checks)

                        if not new_com in self.client.all_commands.keys():
                            self.client.add_command(new_com)
                            loaded += 1

                    except Exception as error:
                        errors += 1
                        error_lst.append(error)

                info(f" * - Command : {loaded} loaded | {errors} error : {error_lst}")

                # Slash

                loaded: int = 0
                errors: int = 0
                error_lst: list = []

                app_groupe = discord.app_commands.Group(name=app_name.lower(), description=f"{len(app.Lib.app.slashs)} commands", guild_ids=self.Lib.store.get_guilds_installed(app_name) if not sys else None)

                dir_comm: list = []
                ndir_comm: list = []

                for command in app.Lib.app.slashs:
                    try:
                        if command.direct_command:
                            dir_comm.append(command)

                        else:
                            ndir_comm.append(command)

                    except Exception as error:
                        errors += 1
                        error_lst.append(error)

                for command in dir_comm:
                    if not command.name in [com.name for com in self.client.tree.get_commands()]:
                        self.client.tree.add_command(command, guilds=([self.client.get_guild(guild_id) for guild_id in self.Lib.store.get_guilds_installed(app_name) if self.client.get_guild(guild_id)!=None]) if not sys else MISSING)
                        loaded += 1

                for command in ndir_comm:
                    if not command.name in [com.name for com in app_groupe.commands]:
                        app_groupe.add_command(command)
                        loaded += 1

                if len(app_groupe.commands) > 0:
                    try:
                        self.client.tree.add_command(app_groupe, guilds=([self.client.get_guild(guild_id) for guild_id in self.Lib.store.get_guilds_installed(app_name) if self.client.get_guild(guild_id)!=None]) if not sys else MISSING)
                    except Exception as e:
                        error(e)
                        
                info(f" * - Slash : {loaded} loaded | {errors} error : {error_lst}\n")

            else:
                warning(" * - Command : Any guild have installed this app, not loaded")
                warning(" * - Slash : Any guild have installed this app, not loaded")

    def get_help(self, ctx: discord_commands.context.Context) -> list:
        """"""
        embeds: list = []
        embed = discord.Embed(title="OS Commands", description=f"Préfix : `{self.prefix}` | Version : `{BOT_VERSION}`", color=discord.Color.red())

        try:
            coms: list = [com for com in self.client.all_commands]
            coms.sort()

            nb: int = 0
            page: int = 1
            nb_page: int = len(coms) // 25

            embed.set_author(name=f'Liste des commandes {(page+"/"+nb_page) if nb_page > 1 else ""}')

            for com in coms:
                #print(com)
                if all([check(ctx) for check in self.client.all_commands[com].checks] + [True]):
                    embed.add_field(name=f"**{com}**", value=f'{self.client.all_commands[com].help if self.client.all_commands[com].help != None else "Aucune aide disponible"}')
                    nb += 1

                if nb == 25:
                    nb: int = 0
                    embeds.append(embed.copy())
                    embed = discord.Embed(title="OS Commands", color=discord.Color.red())
                    embed.set_author(name=f'Liste des commandes {page}/{nb_page}')
                    page += 1

            if nb > 0:
                embeds.append(embed)

        except Exception as error:
            error(error)

        return embeds

    async def send_error(self, ctx: discord.Interaction, error: str, *args, **kwargs):
        embed = discord.Embed(title="Unexpected Error", description=f"DateTime : `{time.localtime(time.time())}`", color=discord.Color.red())

        if ctx is not None:
            embed.set_author(name=f"{ctx.user.name} use {ctx.command}", icon_url=ctx.user.avatar.url)
            embed.add_field(name="ctx info :", value=ctx.data.items())

        embed.add_field(name="error :", value=str(error))
        embed.add_field(name="error :", value=str(error))

        if self.client.owner_id is None:
            return

        user = await self.client.fetch_user(self.client.owner_id)
        await user.send(embed=embed)

    ################################################################
    #                             INIT                             #
    ################################################################

    def __init__(self, token: str = None, log: bool = False, prefix: str = "?", status: list = ["UnderStar OS"]) -> None:
        self.all_app = import_module("app", log=log)

        self.status = cycle(status)
        self.prefix = prefix

        client = discord_commands.Bot(intents=self.intents, command_prefix=prefix, help_command=None)
        client.remove_command('help')

        self.client = client
        Lib = self.Lib

        if token is None:
            try:
                with open(BOT_TOKEN_PATH, "r", encoding="utf8") as f:
                    token = f.readlines()[0].strip()

            except Exception:
                with open(BOT_TOKEN_PATH, "w", encoding="utf8") as f:
                    warning("TOKEN not set, please set token at /token/bot_token file")
                    f.write("TOKEN HERE")
                sys.exit(0)

        self.BOT_TOKEN = token

        # -------------------------------- Slash Command -------------------

        @client.tree.command(name = "info", description = "Donne des infos sur le bot", guild=None)
        async def info_command(ctx:discord.Interaction):
            embed = discord.Embed(title="INFO")
            embed.add_field(name="Version  :", value=f"`{BOT_VERSION}`")
            embed.add_field(name="Ping  :", value=f"` {round(self.client.latency * 1000)} `")
            embed.add_field(name="Time up  :", value=f"<t:{int(self.timer)}:R>")
            await ctx.response.send_message(embed=embed, ephemeral=True)


        # -------------------------------- COMMANDE -------------------------------

        @client.command(name="os-test", help="Envoie une pizza gatuite")
        async def test(ctx:discord_commands.context.Context):
            await ctx.send(":pizza:")


        @client.command(name="os-ping", aliases=["os-ver", "ver", "ping"], help="Donne des infos sur le bot")
        @discord_commands.check(Lib.is_in_staff)
        async def version(ctx:discord_commands.context.Context):
            embed = discord.Embed(title="INFO")
            embed.add_field(name="Version :", value=f"`{BOT_VERSION}`")
            embed.add_field(name="Ping :", value=f"` {round(self.client.latency * 1000)} `")
            embed.add_field(name="Time up :", value=f"<t:{int(self.timer)}:R>")

            await ctx.send(embed=embed)


        @client.command(name="os-help", aliases=["help"], help="Pour avoir ce message")
        async def help(ctx:discord_commands.context.Context,*args):
            if args == ():
                await ctx.send(embeds=self.get_help(ctx))

            else :
                if args[0] in self.all_app.keys():
                    sys_com = False
                    com = self.all_app

                elif args[0] in sys_app.all_app:
                    sys_com = True
                    com = sys_app.all_app

                else:
                    return

                if len(args) == 1:
                    try:
                        await com[args[0]].Lib.help(ctx)

                    except Exception as error:
                        if types(error) == AttributeError:
                            await ctx.send(content=f"L'application `{args[0]}` n'a pas de fonction d'aide")

                        else:
                            await ctx.send(content=f"La fonction d'aide de l'application `{args[0]}` ne fonctionne pas. Merci de contacter son développeur.")

                else:
                    if f"{args[0]}-{args[1]}" in client.all_commands.keys():
                        embed = discord.Embed(title=f"Aide sur la commande `{args[1]}`", description=f"Commande : `{self.prefix}{args[0]}-{args[1]}`", color=discord.Color.red())
                        embed.set_author(name=f'App : {args[0]}')
                        aide: str = client.all_commands[f"{args[0]}-{args[1]}"].help if client.all_commands[f"{args[0]}-{args[1]}"].help!="" else "Pas d'aide pour cette commande"
                        alias: str = ""

                        for command in client.all_commands.keys():
                            if command != f"{args[0]}-{args[1]}" and client.all_commands[command]==client.all_commands[f"{args[0]}-{args[1]}"]:
                                alias += f"{command}, "

                        embed.add_field(name=f"**{aide}**", value=f"Alias : {alias[:-1]}")

                    else:
                        embed = discord.Embed(title=f"La Command `{args[1]}` n'existe pas", description=f"Préfix de l'app : `{self.prefix}{args[0]}-`", color=discord.Color.red())
                        embed.set_author(name=f"App : {args[0]}")
                        # embed.add_field(name=f"**La Command {args[1]} n'existe pas**", value=f"Commande d'aide de l'application {args[0]} : !{args[0]}-help")

                    try:
                        await ctx.send(embed=embed)

                    except Exception as error:
                        error(error)

        # ---------------------------------- EVENTS ------------------------------------

        #@terminal()
        async def manage_event(command, *args, **kwargs):
            for app in list(self.all_app.values()) + list(sys_app.all_app.values()):
                if app:
                    data = getattr(app.Lib.event, command)
                    await data(*args, **kwargs)

                    if app.Lib.app.fusioned:
                        for sub_app in app.Lib.app.fusioned_module:
                            data = getattr(sub_app.Lib.event, command)
                            await data(*args, **kwargs)

        #App Commands
        @client.event
        async def on_raw_app_command_permissions_update(payload):
            await manage_event("on_raw_app_command_permissions_update", payload)

        @client.event
        async def on_app_command_completion(interaction, command):
            await manage_event("on_app_command_completion", interaction, command)

        @client.tree.error
        async def on_app_command_error(ctx: discord.Interaction, error: discord.app_commands.AppCommandError):
            await manage_event("on_app_command_error", ctx, error)

            if isinstance(error, discord.app_commands.CheckFailure):
                await ctx.response.send_message('Tu ne remplis pas les conditions pour executer cette commande.', ephemeral=True)

            elif isinstance(error, discord.app_commands.BotMissingPermissions):
                await ctx.response.send_message('Le bot ne peut pas executer cette commande car il lui manque des autorisations. Merci de contacter le STAFF', ephemeral=True)

            else:
                try:
                    await ctx.response.send_message(content=f"Data :\n{ctx.data}\nError :\n{error}", ephemeral = True)

                except Exception:
                    error(f"Data :\n{ctx.data}\nError :\n{error}")

                await self.send_error(ctx, error)

        #AutoMod
        @client.event
        async def on_automod_rule_create(rule):
            await manage_event("on_automod_rule_create", rule)

        @client.event
        async def on_automod_rule_update(rule):
            await manage_event("on_automod_rule_update", rule)

        @client.event
        async def on_automod_rule_delete(rule):
            await manage_event("on_automod_rule_delete", rule)

        @client.event
        async def on_automod_action(execution):
            await manage_event("on_automod_action", execution)

        #Channels
        @client.event
        async def on_guild_channel_delete(channel):
            await manage_event("on_guild_channel_delete", channel)

        @client.event
        async def on_guild_channel_create(channel):
            await manage_event("on_guild_channel_create", channel)

        @client.event
        async def on_guild_channel_update(before, after):
            await manage_event("on_guild_channel_update", before, after)

        @client.event
        async def on_guild_channel_pins_update(channel, last_pin):
            await manage_event("on_guild_channel_pins_update", channel, last_pin)

        @client.event
        async def on_private_channel_update(before, after):
            await manage_event("on_private_channel_update", before, after)

        @client.event
        async def on_private_channel_pins_update(channel, last_pin):
            await manage_event("on_private_channel_pins_update", channel, last_pin)

        @client.event
        async def on_typing(channel, user, when):
            await manage_event("on_typing", channel, user, when)

        @client.event
        async def on_raw_typing(payload):
            await manage_event("on_raw_typing", payload)

        #Connection
        @client.event
        async def on_connect(self):
            await manage_event("on_connect", self)

        @client.event
        async def on_disconnect(self):
            await manage_event("on_disconnect", self)

        @client.event
        async def on_shard_connect(shard_id):
            await manage_event("on_shard_connect", shard_id)

        @client.event
        async def on_shard_disconnect(shard_id):
            await manage_event("on_shard_disconnect", shard_id)

        #Commande
        @client.event
        async def on_command_error(ctx: discord_commands.Context, error):
            if isinstance(error, discord_commands.MissingRequiredArgument):
                await ctx.send('Please pass in all required arguments')

            elif isinstance(error, discord_commands.CommandOnCooldown):
                value: int = int(f"{error.retry_after:.0f}")
                message: str = "Try again in "
                message += convert_time(value)

                em = discord.Embed(title="Slow it down bro!", description=message)
                await ctx.send(embed=em)

            else:
                await self.send_error(None, error, ctx.args)

            await manage_event("on_command_error", ctx, error)

        #Debug
        @client.event
        async def on_error(event, *args, **kwargs):
            await manage_event("on_error", event, *args, **kwargs)
            await self.send_error(None, event, args, kwargs)

        @client.event
        async def on_socket_event_type(event_type):
            await manage_event("on_socket_event_type", event_type)

        @client.event
        async def on_socket_raw_receive(msg):
            await manage_event("on_socket_raw_receive", msg)

        @client.event
        async def on_socket_raw_send(payload):
            await manage_event("on_socket_raw_send", payload)

        #Gateway
        @client.event
        async def on_ready():
            client.info = await client.application_info()
            change_status.start()

            #maintenance.start()
            await self.import_apps(True)
            await self.import_apps()
            
            info(" * Bot Starting...")
            info(f" * version : {programmer} {BOT_VERSION}")
            info(f" * Logged in as : {client.user.name}")
            info(f" * ID : {client.user.id}")

            await client.tree.sync()

            with open(GUILD_FILE, encoding="utf8") as f:
                data = json.load(f)

            for guild in client.guilds:
                if "sync" in sys.argv:
                    client.tree.copy_global_to(guild=discord.Object(id=guild.id))

                await client.tree.sync(guild=discord.Object(id=guild.id))

                if str(guild.id) not in data.keys():
                    data.update({str(guild.id):{"apps":[], "admin":[guild.owner.id], "password":None, "theme":"bleu"}})

                    with open(GUILD_FILE, "w", encoding="utf8") as f:
                        json.dump(data, fp=f)

            if "sync" in sys.argv:
                os.execv(sys.executable, ["None", os.path.basename(sys.argv[0])])

            await manage_event("on_ready")

        @client.event
        async def on_resumed():
            await manage_event("on_resumed")

        @client.event
        async def on_shard_ready(shard_id):
            await manage_event("on_shard_ready", shard_id)

        @client.event
        async def on_shard_resumed(shard_id):
            await manage_event("on_shard_resumed", shard_id)

        #Guilds
        @client.event
        async def on_guild_available(guild):
            await manage_event("on_guild_available", guild)

        @client.event
        async def on_guild_unavailable(guild):
            await manage_event("on_guild_unavailable", guild)

        @client.event
        async def on_guild_join(guild):
            with open(GUILD_FILE, encoding="utf8") as f:
                data = json.load(f)

            if str(guild.id) in data.keys():
                data.update({str(guild.id):{"apps":[], "admin":[guild.owner.id], "password":None, "theme":"bleu"}})

                with open(GUILD_FILE, "w", encoding="utf8") as f:
                    json.dump(data, fp=f)

            await manage_event("on_guild_join", guild)

        @client.event
        async def on_guild_remove(guild):
            await manage_event("on_guild_remove", guild)

        @client.event
        async def on_guild_update(before, after):
            await manage_event("on_guild_update", before, after)

        @client.event
        async def on_guild_emojis_update(guild, before, after):
            await manage_event("on_guild_emojis_update", guild, before, after)

        @client.event
        async def on_guild_stickers_update(guild, before, after):
            await manage_event("on_guild_stickers_update", guild, before, after)

        @client.event
        async def on_invite_create(invite):
            await manage_event("on_invite_create", invite)

        @client.event
        async def on_invite_delete(invite):
            await manage_event("on_invite_delete", invite)

        #Integrations
        @client.event
        async def on_integration_create(integration):
            await manage_event("on_integration_create", integration)

        @client.event
        async def on_integration_update(integration):
            await manage_event("on_integration_update", integration)

        @client.event
        async def on_guild_integrations_update(guild):
            await manage_event("on_guild_integrations_update", guild)

        @client.event
        async def on_webhooks_update(channel):
            await manage_event("on_webhooks_update", channel)

        @client.event
        async def on_raw_integration_delete(payload):
            await manage_event("on_raw_integration_delete", payload)

        #Interactions
        @client.event
        async def on_interaction(interaction):
            await manage_event("on_interaction", interaction)

        #Members
        @client.event
        async def on_member_join(member):
            await manage_event("on_member_join", member)

        @client.event
        async def on_member_remove(member):
            await manage_event("on_member_remove", member)

        @client.event
        async def on_raw_member_remove(payload):
            await manage_event("on_raw_member_remove", payload)

        @client.event
        async def on_member_update(before, after):
            await manage_event("on_member_update", before, after)

        @client.event
        async def on_user_update(before, after):
            await manage_event("on_user_update", before, after)

        @client.event
        async def on_member_ban(guild, user):
            await manage_event("on_member_ban", guild, user)

        @client.event
        async def on_member_unban(guild, user):
            await manage_event("on_member_unban", guild, user)

        @client.event
        async def on_presence_update(before, after):
            await manage_event("on_presence_update", before, after)

        #Messages
        @client.event
        async def on_message(message):
            await client.process_commands(message)
            await manage_event("on_message", message)

        @client.event
        async def on_message_edit(before, after):
            await manage_event("on_message_edit", before, after)

        @client.event
        async def on_message_delete(message):
            await manage_event("on_message_delete", message)

        @client.event
        async def on_bulk_message_delete(messages):
            await manage_event("on_bulk_message_delete", messages)

        @client.event
        async def on_raw_message_edit(payload):
            await manage_event("on_raw_message_edit", payload)

        @client.event
        async def on_raw_message_delete(payload):
            await manage_event("on_raw_message_delete", payload)

        @client.event
        async def on_raw_bulk_message_delete(payload):
            await manage_event("on_raw_bulk_message_delete", payload)

        #Reactions
        @client.event
        async def on_reaction_add(reaction, user):
            await manage_event("on_reaction_add", reaction, user)

        @client.event
        async def on_reaction_remove(reaction, user):
            await manage_event("on_reaction_remove", reaction, user)

        @client.event
        async def on_reaction_clear(message, reactions):
            await manage_event("on_reaction_clear", message, reactions)

        @client.event
        async def on_reaction_clear_emoji(reaction):
            await manage_event("on_reaction_clear_emoji", reaction)

        @client.event
        async def on_raw_reaction_add(payload):
            await manage_event("on_raw_reaction_add", payload)

        @client.event
        async def on_raw_reaction_remove(payload):
            await manage_event("on_raw_reaction_remove", payload)

        @client.event
        async def on_raw_reaction_clear(payload):
            await manage_event("on_raw_reaction_clear", payload)

        @client.event
        async def on_raw_reaction_clear_emoji(payload):
            await manage_event("on_raw_reaction_clear_emoji", payload)

        #Roles
        @client.event
        async def on_guild_role_create(role):
            await manage_event("on_guild_role_create", role)

        @client.event
        async def on_guild_role_delete(role):
            await manage_event("on_guild_role_delete", role)

        @client.event
        async def on_guild_role_update(before, after):
            await manage_event("on_guild_role_update", before, after)

        #Scheduled Events
        @client.event
        async def on_scheduled_event_create(event):
            await manage_event("on_scheduled_event_create", event)

        @client.event
        async def on_scheduled_event_delete(event):
            await manage_event("on_scheduled_event_delete", event)

        @client.event
        async def on_scheduled_event_update(before, after):
            await manage_event("on_scheduled_event_update", before, after)

        @client.event
        async def on_scheduled_event_user_add(event, user):
            await manage_event("on_scheduled_event_user_add", event, user)

        @client.event
        async def on_scheduled_event_user_remove(event, user):
            await manage_event("on_scheduled_event_user_remove", event, user)

        #Stages
        @client.event
        async def on_stage_instance_create(stage_instance):
            await manage_event("on_stage_instance_create", stage_instance)

        @client.event
        async def on_stage_instance_delete(stage_instance):
            await manage_event("on_stage_instance_delete", stage_instance)

        @client.event
        async def on_stage_instance_update(before, after):
            await manage_event("on_stage_instance_update", before, after)

        #Threads
        @client.event
        async def on_thread_create(thread):
            await manage_event("on_thread_create", thread)

        @client.event
        async def on_thread_join(thread):
            await manage_event("on_thread_join", thread)

        @client.event
        async def on_thread_update(before, after):
            await manage_event("on_thread_update", before, after)

        @client.event
        async def on_thread_remove(thread):
            await manage_event("on_thread_remove", thread)

        @client.event
        async def on_thread_delete(thread):
            await manage_event("on_thread_delete", thread)

        @client.event
        async def on_raw_thread_update(payload):
            await manage_event("on_raw_thread_update", payload)

        @client.event
        async def on_raw_thread_delete(payload):
            await manage_event("on_raw_thread_delete", payload)

        @client.event
        async def on_thread_member_join(member):
            await manage_event("on_thread_member_join", member)

        @client.event
        async def on_thread_member_remove(member):
            await manage_event("on_thread_member_remove", member)

        @client.event
        async def on_raw_thread_member_remove(payload):
            await manage_event("on_raw_thread_member_remove", payload)

        #Voice
        @client.event
        async def on_voice_state_update(member, before, after):
            await manage_event("on_voice_state_update", member, before, after)

        # ----------------------------COMMANDE MAINTENANCE----------------------------------
        @client.command(name="triger_event", help="Simule un event")
        @discord_commands.check(Lib.is_in_staff)
        async def triger_event(ctx:discord_commands.context.Context, event_name, *args):
            if event_name == "on_member_join" or event_name == "on_member_remove":
                member = ctx.author
                await manage_event(event_name, member)

            else:
                await manage_event(event_name)

        @client.command(name="restart", help="Pour restart le bot")
        @discord_commands.check(Lib.is_in_staff)
        async def reboot(ctx:discord_commands.context.Context):
            await client.change_presence(activity=discord.Game("Restarting..."), status=discord.Status.dnd)

            await ctx.send("Restarting bot")
            os.execv(sys.executable, ["None", os.path.basename(sys.argv[0])])

        @client.command(help="stop le bot")
        @discord_commands.check(Lib.is_in_staff)
        async def stop(ctx:discord_commands.context.Context):
            await ctx.send("Stopping")
            await client.change_presence(activity=discord.Game("Shutting down..."), status=discord.Status.dnd)
            exit(1)
            quit()

        @client.command(aliases=["upt"], help="Pour update le bot")
        @discord_commands.check(Lib.is_in_staff)
        async def update(ctx:discord_commands.context.Context):
            await ctx.send("updating code !")
            await client.change_presence(activity=discord.Game("Updating..."), status=discord.Status.idle)

            val = os.system(f"start {UPDATE_FILE}")

            await client.change_presence(activity=discord.Game("Back from updt !"), status=discord.Status.online)

            if val == 0:
                await ctx.send("Done")
                await client.close()

            else:
                await ctx.send("Error!")
                exit(0)

        # -------------------------------------- TASKS -----------------------------------
        @discord_tasks.loop(seconds=127)
        async def change_status():
            if "sync" in sys.argv:
                await client.change_presence(activity=discord.Game("Re-Sync..."), status=discord.Status.dnd)

            else:
                await client.change_presence(activity=discord.Game(next(self.status)))
