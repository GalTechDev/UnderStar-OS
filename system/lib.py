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


    def set_app_name(self, app_name):
        self.app_name = app_name
        self.save.app_name = app_name
        self.app_path = f"app/{app_name}/"
        if self.app.fusioned:
            for mod in self.app.fusioned_module:
                mod.Lib.set_app_name(app_name)

    def init_client(self,bot_client):
        self.client = bot_client
        

    def is_in_staff(self, ctx:discord.Interaction, direct_author=False): 
        if type(ctx)==discord.Interaction:
            user = ctx.user
        else:
            user = ctx.author
        if user.id in self.guilds.get_admin_guilds(guild = ctx.guild_id):
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
        await client.change_presence(activity=activity, status=status)

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
        if path=="":
            with open(f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}", "x"):
                pass
        else:
            with open(f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}", "x"):
                pass
        pass

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
            
        with open(path, f"r{'b' if binary_mode else ''}") as file:
            return file.read()

    def write(self, name, path="", data="", binary_mode=False):
        if path=="":
            path = f"{self.save_path}/{self.app_name}/{name}"
        else:
            path = f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"

        with open(path, f"w{'b' if binary_mode else ''}") as file:
            file.write(data)

    def get_files(self, path=""):
        return os.listdir(f"{self.save_path}/{self.app_name}/{path}")

    def remove_file(self, name, path=""):
        if path=="":
            os.remove(f"{self.save_path}/{self.app_name}/{name}")
        else:
            os.remove(f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}")
        pass

    def add_folder(self, path="", ignor_exception=True):
        try:
            os.mkdir(f"{self.save_path}/{self.app_name}/{path}")
        except:
            if not ignor_exception:
                raise Exception(f"Path: {path} can't be create")


        pass

    def remove_folder(self, path=""):
        shutil.rmtree(f"{self.save_path}/{self.app_name}/{path}")
        pass

    def get_tree(self, path=""):
        tree={}
        for folder in os.listdir(f"{self.save_path}/{self.app_name}/{path}"):
            if os.path.isdir(f"{self.save_path}/{self.app_name}/{path}/{folder}"):
                tree[folder]=self.get_tree(f"{path}/{folder}")
        return tree

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