import discord
from .types import *
import json
import importlib
import glob
import os
import pkg_resources
import sys

LANGAGE = "fr"

THEME = {"gris": discord.Color.dark_grey, "bleu": discord.Color.blue, "rouge": discord.Color.red, "vert": discord.Color.green, "jaune":discord.Color.yellow}

async def valide_intaraction(interaction: discord.Interaction):
    try:
        await interaction.response.send_message()
    except Exception as error:
        pass

chemin_fichier = pkg_resources.resource_filename(__name__, '.version')

with open(os.path.join(chemin_fichier.removesuffix(os.path.join("system","lib",".version")),".version"), 'r') as f:
    BOT_VERSION = f.read()

def import_module(folder: str, log=False, catch_error=True, directory = None, found_sub_dir = True):
    """
    Import a module.

    The 'directory' argument is required when performing a relative import. It specifies the package to use as the anchor point from which to resolve the relative import to an absolute import.
    """
    # Parcours des apps dans le répertoire du package
    if log:
        print(f" * Import Module Start :")
    modules = {}
    path = os.path.join(folder.replace(".", "\\"), "*", "__init__.py") if found_sub_dir else os.path.join(folder.replace(".", "\\"), "*__init__.py")
    #print(path, glob.glob(path, recursive=True, root_dir=directory))
    for file_path in glob.glob(path, recursive=True, root_dir=directory):
        # Obtention du nom du module à partir du chemin de l'app
        if found_sub_dir:
            module_name = file_path[len(folder)+1:-len("*__init__.py")]
        else:
            module_name = folder
            
        try:
            if directory not in sys.path and directory!=None:
                sys.path.append(os.path.join(directory))
            # Importation dynamique du module
            module_path = file_path.replace("/", ".").replace("\\", ".")
            module = importlib.import_module(f'{module_path[:-3]}')
            #print(module_path[:-3])
            # Ajout du module au dictionnaire
            modules.update({module_name:module})
            if log:
                print(f" *  - imported {module_name}")
            
        except Exception as e:
            if log:
                print(f" *  - failled importing {module_name} error : {e}")
            if not catch_error:
                raise e
    
    if log:    
        print(f" * Import Module Finish")
    return modules

def convert_time(value: int):
        """"""
        val3, val2, val = 0, value//60, value % 60
        message = f"{val2}min {val}s."

        if val2 > 60:
            val3, val2 = val2//60, val2 % 60
            message = f"{val3}h {val2}min {val}s."

        return message

class Task:
    """"""
    def __init__(self,function,seconds: float = MISSING, minutes: float = MISSING, hours: float = MISSING, time: Union[datetime.time, Sequence[datetime.time]] = MISSING, count = None, reconnect: bool = True) -> None:
        self.function=function
        self.seconds=seconds
        self.minutes=minutes
        self.hours=hours
        self.count=count
        self.reconnect=reconnect
        self.time=time

class Guilds:
    """"""
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