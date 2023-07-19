import discord
from .types import *
import json
import importlib
import glob
import os
import pkg_resources

LANGAGE = "fr"

THEME = {"gris": discord.Color.dark_grey, "bleu": discord.Color.blue, "rouge": discord.Color.red, "vert": discord.Color.green, "jaune":discord.Color.yellow}

async def valide_intaraction(interaction: discord.Interaction):
    try:
        await interaction.response.send_message()
    except Exception as error:
        pass

chemin_fichier = pkg_resources.resource_filename(__name__, '.version')

with open(chemin_fichier.removesuffix("understar2/system/lib/.version")+".version", 'r') as f:
    BOT_VERSION = f.read()

def import_module(folder: str, log=False, catch_error=True):
    # Parcours des apps dans le répertoire du package
    if log:
        print(f" * Import Module Start :")
    modules = {}
    for file_path in glob.glob(os.path.join(folder.replace(".", "/"), "*/__init__.py"), recursive=True):
        # Obtention du nom du module à partir du chemin de l'app
        module_name = os.path.basename(file_path)

        try:
            # Importation dynamique du module
            module = importlib.import_module(f'{file_path.replace("/", ".")}'[:-3])
            
            # Ajout du module au dictionnaire
            modules.update({file_path.removesuffix('/__init__.py').removeprefix(folder.replace('.', '/'))[1:]:module})
            if log:
                print(f" *  - imported {file_path.removesuffix('/__init__.py').removeprefix(folder.replace('.', '/'))[1:]}")
            
        except Exception as e:
            if log:
                print(f" *  - failled importing {file_path.removesuffix('/__init__.py').removeprefix(folder.replace('.', '/'))[1:]} error : {e}")
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