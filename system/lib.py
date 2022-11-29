import discord
from discord.ext import commands as discord_commands
from discord.ext import tasks as discord_tasks
import json
import save.system.installed_app as installed_app

langage = "Francais"
client = None

def init_client(bot_client):
    global client
    client = bot_client

class App:
    def __init__(self) -> None:
        self.commands = []
        self.slashs = []
        self.task = []
    
    def command(self, name=None, help_text: str="", aliases: (list[str])=[], checks=[], force_name: bool = False):
        def apply(funct):
            self.commands.append(Command(name if name != None else funct.__name__ , funct, help_text, aliases, checks, force_name))
            return funct
        return apply

    def slash(self, description: str, name: str = None, guild = discord.utils.MISSING, guilds: list = discord.utils.MISSING, force_name: bool = False):
        def apply(funct):
            self.slashs.append(Slash(name if name != None else funct.__name__ , description, funct, guild, guilds, force_name))
            return funct
        return apply

    def tasks(self, seconds: int = discord_tasks.MISSING, minutes: int = discord_tasks.MISSING, hours: int = discord_tasks.MISSING, time=discord_tasks.MISSING, count = None, reconnect: bool = True):
        def apply(funct):
            self.task.append(Task(funct, seconds, minutes, hours, time, count, reconnect))
            return funct
        return apply

    def fusion(self, apps):
        for app in apps:
            self.commands+=app.app.commands
            self.task+=app.app.task
            self.slashs+=app.app.slashs

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


def is_in_staff(ctx:discord.Interaction, direct_author=False):
    if type(ctx)==discord.Interaction:
        au_id = ctx.user.id
    else:
        au_id = ctx.author.id
    if au_id in [608779421683417144]:
        return True 
    if not direct_author:
        member = ctx.message.author
    else:
        member = ctx.author
    roles = [role.name for role in member.roles]
    admins = ["Admin", "Modo", "Bot Dev"]

    for role in roles:
        if role in admins:
            return True

def get_lang_name():
    with open("system/lang/ref.json") as file:
        data = json.load(file)
    return data

def get_lang(lang = langage):
    ref = get_lang_name()
    lang_txt = ref[lang]
    with open(f"system/lang/{lang_txt}.txt") as file:
        all_text = file.readlines()
    return all_text

def get_lang_ref(ref, lang = langage):
    all_ref = get_lang(lang)
    if type(ref) == int:
        return all_ref[ref][:-1]
    elif type(ref) == list:
        return [all_ref[one_ref][:-1] for one_ref in ref]
    else:
        raise Exception

class App_store:
    def __init__(self) -> None:
        pass

    def get_apps() -> dict:
        """Give a dict object {"app_name":"app_link",}"""
        with open("save/system/app_store.json") as file:
            data = json.load(file)
        return data
        
    def get_installed():
        return installed_app.all_app

    def is_in_store(app_name):
        apps = App_store.get_apps()
        return app_name in list(apps.keys())
    
    def is_installed(app_name):
        apps = App_store.get_installed()
        return app_name in list(apps.keys())

    def add_link(app_name, app_link):
        pass

    