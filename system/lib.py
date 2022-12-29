import discord
from discord.ext import commands as discord_commands
from discord.ext import tasks as discord_tasks
import json
import save.system.installed_app as installed_app
import sys
import os
import shutil
import googletrans


langage = "fr"
client = None

theme = {"gris": discord.Color.dark_grey, "bleu": discord.Color.blue, "rouge": discord.Color.red, "vert": discord.Color.green, "jaune":discord.Color.yellow}

def init_event():
    pass

class Lib_UsOS:
    def __init__(self) -> None:
        self.app = App()
        self.app_name = ""
        self.client: discord_commands.bot = None
        self.store = App_store()
        self.save = Save(self.app_name)
        self.guilds = Guilds()
        self.trad = Trad()
        self.event = Event()


    def set_app_name(self, app_name):
        self.app_name = app_name
        self.save.app_name = app_name
        self.app_path = f"app/{app_name}/"
        if self.app.fusioned:
            for mod in self.app.fusioned_module:
                mod.Lib.set_app_name(app_name)

    def init_client(self,bot_client):
        self.client = bot_client
        if self.app.fusioned:
            for app in self.app.fusioned_module:
                app.Lib.init_client(bot_client)
        
    def is_in_staff(self, ctx:discord.Interaction, direct_author=False): 
        if type(ctx)==discord.Interaction:
            user = ctx.user
        else:
            user = ctx.author
        if user.id in self.guilds.get_admin_guilds(guild = ctx.guild_id if type(ctx)==discord.Interaction else ctx.guild.id):
            return True 

        roles = [role.name for role in user.roles]
        admins = ["Admin", "Modo", "Bot Dev"]

        for role in roles:
            if role in admins:
                return True

    def get_lang_name(self):
        with open("system/lang/ref.json") as file:
            data = json.load(file)
        return data

    def get_lang(self, lang = langage):
        ref = self.get_lang_name()
        lang_txt = ref[lang]
        with open(f"system/lang/{lang_txt}.txt") as file:
            all_text = file.readlines()
        return all_text

    def get_lang_ref(self, ref, lang = langage):
        all_ref = self.get_lang(lang)
        if type(ref) == int:
            return all_ref[ref][:-1]
        elif type(ref) == list:
            return [all_ref[one_ref][:-1] for one_ref in ref]
        else:
            raise Exception

    async def change_presence(self, activity, status):
        await self.client.change_presence(activity=activity, status=status)

class App:
    def __init__(self) -> None:
        self.commands = []
        self.slashs = []
        self.task = []
        self.help_com = None
        self.fusioned = False
        self.fusioned_module = []
    
    def command(self, name=None, help_text: str="", aliases: (list[str])=[], checks=[], force_name: bool = False):
        def apply(funct):
            self.commands.append(Command(name if name != None else funct.__name__ , funct, help_text, aliases, checks, force_name))
            return funct
        return apply

    def slash(self, description: str, name: str = None, guild = discord.app_commands.tree.MISSING, guilds: list = discord.app_commands.tree.MISSING, force_name: bool = False):
        def apply(funct):
            self.slashs.append(Slash(name if name != None else funct.__name__ , description, funct, guild, guilds, force_name))
            return funct
        return apply

    def tasks(self, seconds: int = discord_tasks.MISSING, minutes: int = discord_tasks.MISSING, hours: int = discord_tasks.MISSING, time=discord_tasks.MISSING, count = None, reconnect: bool = True):
        def apply(funct):
            self.task.append(Task(funct, seconds, minutes, hours, time, count, reconnect))
            return funct
        return apply

    def help(self):
        def apply(funct):
            self.help_com = funct
            return funct
        return apply

    def fusion(self, apps):
        self.fusioned = True
        self.fusioned_module+=apps
        for app in apps:
            self.commands+=app.Lib.app.commands
            self.task+=app.Lib.app.task
            self.slashs+=app.Lib.app.slashs
            self.help_com = app.Lib.app.help_com

class Slash:
    def __init__(self, name: str, description: str, command, guild = discord.app_commands.tree.MISSING, guilds: list = discord.app_commands.tree.MISSING, force_name: bool = False) -> None:
        self.name=name.replace(" ", "-")
        self.command=command
        self.description=description
        self.guild=guild
        self.guilds=guilds
        self.force_name = force_name
        
class Command:
    def __init__(self, name:str, command, help_text: str="",aliases: (list[str])=[],checks=[], force_name: bool = False) -> None:
        self.name=name.replace(" ", "-")
        self.command=command
        self.help = help_text if help_text!="" else "Aucune aide disponible"
        self.aliases=aliases
        self.checks=checks
        self.force_name = force_name

class Task:
    def __init__(self,fonction,seconds: int = discord_tasks.MISSING, minutes: int = discord_tasks.MISSING, hours: int = discord_tasks.MISSING, time=discord_tasks.MISSING, count = None, reconnect: bool = True) -> None:
        self.fonction=fonction
        self.seconds=seconds
        self.minutes=minutes
        self.hours=hours
        self.count=count
        self.reconnect=reconnect
        self.time=time

class App_store:
    def __init__(self) -> None:
        pass

    def get_apps(self) -> dict:
        """Give a dict object {"app_name":"app_link",}"""
        with open("save/system/app_store.json") as file:
            data = json.load(file)
        return data
        
    def get_installed(self):
        return installed_app.all_app

    def is_in_store(self, app_name):
        apps = self.get_apps()
        return app_name in list(apps.keys())
    
    def is_downloaded(self, app_name):
        apps = self.get_installed()
        return app_name in list(apps.keys())

    def is_installed(self, app_name, guild_id):
        with open("save/system/guilds.json") as file:
            data = json.load(file)
        return app_name in data[str(guild_id)]["apps"]

    def add_link(self, app_name, app_link):
        file_path="save/system/app_store.json"
        with open(file_path) as file:
            store = json.load(file)
            
        store[app_name]=app_link

        with open(file_path, "w") as file:
            file.write(json.dumps(store))

class Save:
    def __init__(self, app_name) -> None:
        self.path = None
        self.app_name = app_name
        self.save_path = "save/app"

    def add_file(self, name, path="", over_write=False):
        """ajoute un fichier à sauvegarder"""
        try:
            if path=="":
                full_path=f"{self.save_path}/{self.app_name}/{name}"
            else:
                full_path=f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"
                
            with open(full_path, "x"):
                pass

        except (FileExistsError):
            if over_write:
                if path=="":
                    full_path=f"{self.save_path}/{self.app_name}/{name}"
                else:
                    full_path=f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"
                os.remove(full_path)
                self.add_file(name,path,over_write)
            else: 
                raise FileExistsError

    def open(self, name, path=""):
        if path=="":
            path = f"{self.save_path}/{self.app_name}/{name}"
        else:
            path = f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"
            
        with open(path) as file:
            return file

    def read(self, name, path="", binary_mode=False):
        if path=="":
            path = f"{self.save_path}/{self.app_name}/{name}"
        else:
            path = f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"
            
        with open(path, 'rb' if binary_mode else 'r') as file:
            return file.read()

    def write(self, name, path="", data="", binary_mode=False):
        if path=="":
            path = f"{self.save_path}/{self.app_name}/{name}"
        else:
            path = f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"

        with open(path, 'wb' if binary_mode else 'w') as file:
            file.write(data)

    def get_files(self, path=""):
        return os.listdir(f"{self.save_path}/{self.app_name}/{path}")

    def remove_file(self, name, path=""):
        if path=="":
            path = f"{self.save_path}/{self.app_name}/{name}"
        else:
            path = f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"
        
        os.remove(f"{path}/{self.app_name}/{name}")
        

    def add_folder(self, path="", ignor_exception=True):
        try:
            os.mkdir(f"{self.save_path}/{self.app_name}/{path}")
        except:
            if not ignor_exception:
                raise Exception(f"Path: {path} can't be create")

    def remove_folder(self, path=""):
        shutil.rmtree(f"{self.save_path}/{self.app_name}/{path}")
        pass

    def get_tree(self, path=""):
        tree={}
        for folder in os.listdir(f"{self.save_path}/{self.app_name}/{path}"):
            if os.path.isdir(f"{self.save_path}/{self.app_name}/{path}/{folder}"):
                tree[folder]=self.get_tree(f"{path}/{folder}")
        return tree

    def get_full_path(self, name, path=""):
        if path=="":
            path=(f"{self.save_path}/{self.app_name}/{name}")
        else:
            path=(f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}")
        return path

class Guilds:
    def __init__(self) -> None:
        pass
        
    def get_app_guilds(self, app_name=None, guild=None):
        if not app_name==None and not guild==None:
            raise Exception("app_name and guild cannot be mixed")

        with open("save/system/guilds.json") as file:
            data = json.load(file)

        if app_name==None and not guild==None:
            return data[str(guild)]["apps"]

        apps={}
        for guild_id in list(data.keys()):
            for app in data[str(guild_id)]["apps"]:
                if app not in list(apps.keys()):
                    apps[app]=[discord.Object(id=int(guild_id))]
                else:
                    apps[app].append(guild_id)

        if app_name==None:
            return apps
        elif app_name in list(apps.keys()):
            return apps[app_name]
        else:
            return []

    def get_admin_guilds(self, admin_id=None, guild=None):
        if not admin_id==None and not guild==None:
            raise Exception("admin_id and guild cannot be mixed")

        with open("save/system/guilds.json") as file:
            data = json.load(file)

        if admin_id==None and not guild==None:
            return data[str(guild)]["admin"]

        apps={}
        for guild_id in list(data.keys()):
            for app in data[str(guild_id)]["admin"]:
                if app not in list(apps.keys()):
                    apps[app]=[discord.Object(id=int(guild_id))]
                else:
                    apps[app].append(guild_id)

        if admin_id==None:
            return apps
        elif admin_id in list(apps.keys()):
            return apps[admin_id]
        else:
            return []

    def get_theme_guilds(self, theme_color=None, guild=None):
        if not theme_color==None and not guild==None:
            raise Exception("theme_color and guild cannot be mixed")

        with open("save/system/guilds.json") as file:
            data = json.load(file)

        if theme_color==None and not guild==None:
            return data[str(guild)]["theme"]

        apps={}
        for guild_id in list(data.keys()):
            for app in data[str(guild_id)]["theme"]:
                if app not in list(apps.keys()):
                    apps[app]=[discord.Object(id=int(guild_id))]
                else:
                    apps[app].append(guild_id)

        if theme_color==None:
            return apps
        elif theme_color in list(apps.keys()):
            return apps[theme_color]
        else:
            return []

class Trad:
    def __init__(self) -> None:
        self.trad = googletrans.Translator()

    def __add__(self, text):
        try:
            text = self.trad.translate(text, dest=langage).text
            print(text)
        except Exception as error:
            print(error)
        return text

class Event:
    def __init__(self) -> None:
        self.func = self.__dict__
        self.on_ready = self.on_ready

    def event(self):
        def apply(funct: function) -> function:
            if funct.__name__ in self.func.keys():
                self.func[funct.__name__] = funct
                return funct
            else:
                raise Exception(f"Event : {funct.__name__} are unknow")
        return apply

    #App Commands

    def on_raw_app_command_permissions_update(self, payload):
        pass

    def on_app_command_completion(self, interaction, command):
        pass

    #AutoMod

    def on_automod_rule_create(self, rule):
        pass

    def on_automod_rule_update(self, rule):
        pass

    def on_automod_rule_delete(self, rule):
        pass

    def on_automod_action(self, execution):
        pass

    #Channels

    def on_guild_channel_delete(self, channel):
        pass

    def on_guild_channel_create(self, channel):
        pass

    def on_guild_channel_update(self, before, after):
        pass
    
    def on_guild_channel_pins_update(self, channel, last_pin):
        pass

    def on_private_channel_update(self, before, after):
        pass

    def on_private_channel_pins_update(self, channel, last_pin):
        pass

    def on_typing(self, channel, user, when):
        pass

    def on_raw_typing(self, payload):
        pass

    #Connection

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_shard_connect(self, shard_id):
        pass

    def on_shard_disconnect(self, shard_id):
        pass

    #Debug

    def on_error(self, event, *args, **kwargs):
        pass

    def on_socket_event_type(self, event_type):
        pass

    def on_socket_raw_receive(self, msg):
        pass

    def on_socket_raw_send(self, payload):
        pass

    #Gateway

    def on_ready(self):
        pass

    def on_resumed(self):
        pass

    def on_shard_ready(self, shard_id):
        pass

    def on_shard_resumed(self, shard_id):
        pass

    #Guilds

    def on_guild_available(self, guild):
        pass

    def on_guild_unavailable(self, guild):
        pass

    def on_guild_join(self, guild):
        pass

    def on_guild_remove(self, guild):
        pass

    def on_guild_update(self, before, after):
        pass

    def on_guild_emojis_update(self, guild, before, after):
        pass

    def on_guild_stickers_update(self, guild, before, after):
        pass

    def on_invite_create(self, invite):
        pass

    def on_invite_delete(self, invite):
        pass

    #Integrations

    def on_integration_create(self, integration):
        pass

    def on_integration_update(self, integration):
        pass

    def on_guild_integrations_update(self, guild):
        pass

    def on_webhooks_update(self, channel):
        pass

    def on_raw_integration_delete(self, payload):
        pass

    #Interactions

    def on_interaction(self, interaction):
        pass

    #Members

    def on_member_join(self, member):
        pass

    def on_member_remove(self, member):
        pass

    def on_raw_member_remove(self, payload):
        pass

    def on_member_update(self, before, after):
        pass

    def on_user_update(self, before, after):
        pass

    def on_member_ban(self, guild, user):
        pass

    def on_member_unban(self, guild, user):
        pass

    def on_presence_update(self, before, after):
        pass

    #Messages

    def on_message(self, message):
        pass

    def on_message_edit(self, before, after):
        pass

    def on_message_delete(self, message):
        pass

    def on_bulk_message_delete(self, messages):
        pass

    def on_raw_message_edit(self, payload):
        pass

    def on_raw_message_delete(self, payload):
        pass

    def on_raw_bulk_message_delete(self, payload):
        pass

    #Reactions

    def on_reaction_add(self, reaction, user):
        pass

    def on_reaction_remove(self, reaction, user):
        pass

    def on_reaction_clear(self, message, reactions):
        pass

    def on_reaction_clear_emoji(self, reaction):
        pass

    def on_raw_reaction_add(self, payload):
        pass

    def on_raw_reaction_remove(self, payload):
        pass

    def on_raw_reaction_clear(self, payload):
        pass

    def on_raw_reaction_clear_emoji(self, payload):
        pass

    #Roles

    def on_guild_role_create(self, role):
        pass

    def on_guild_role_delete(self, role):
        pass

    def on_guild_role_update(self, before, after):
        pass

    #Scheduled Events

    def on_scheduled_event_create(self, event):
        pass

    def on_scheduled_event_delete(self, event):
        pass

    def on_scheduled_event_update(self, before, after):
        pass

    