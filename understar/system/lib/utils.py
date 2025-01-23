import discord
from .types import MISSING, Union, datetime, Sequence
import json
import importlib
import glob
import os
import pkg_resources
import sys
from logging import info, warning

LANGAGE = "fr"
THEME = {"gris": discord.Color.dark_grey, "bleu": discord.Color.blue, "rouge": discord.Color.red, "vert": discord.Color.green, "jaune":discord.Color.yellow}
chemin_fichier = pkg_resources.resource_filename(__name__, '.version')

with open(os.path.join(chemin_fichier.removesuffix(os.path.join("system", "lib", ".version")), ".version"), 'r', encoding="utf8") as f:
    BOT_VERSION = f.read()


async def valide_intaraction(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
        #await interaction.response.send_message()

    except Exception:
        pass


def import_module(folder: str, log: bool = False, catch_error: bool = False, directory: str = None, found_sub_dir: bool = True):
    """
    Import a module.

    The 'directory' argument is required when performing a relative import. It specifies the package to use as the anchor point from which to resolve the relative import to an absolute import.
    """
    # Parcours des apps dans le répertoire du package

    if log:
        info(" * Import Module Start :")

    modules: dict = {}
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
            # print(module_path[:-3])
            # Ajout du module au dictionnaire
            modules.update({module_name:module})

            if log:
                info(f" *  - imported {module_name}")

        except Exception as e:
            if log:
                warning(f" *  - failled importing {module_name} error : {e}")

            if not catch_error:
                raise e

    if log:
        info(" * Import Module Finish")

    return modules

def convert_time(value: int):
        """"""
        val3, val2, val = 0, value//60, value % 60
        str_time: str = f"00:{val2}:{val}"

        if val2 > 60:
            val3, val2 = val2//60, val2 % 60
            str_time = f"{val3}:{val2}:{val}"

        return str_time

class Task:
    """"""
    def __init__(self, function, seconds: float = MISSING, minutes: float = MISSING, hours: float = MISSING, time: Union[datetime.time, Sequence[datetime.time]] = MISSING, count = None, reconnect: bool = True) -> None:
        self.function = function
        self.seconds: float = seconds
        self.minutes: float = minutes
        self.hours: float = hours
        self.count = count
        self.reconnect: bool = reconnect
        self.time = time

class Guilds:
    """"""
    def __init__(self) -> None:
        self.guilds_path = os.path.join("save", "system", "guilds.json")

    def get_app_guilds(self, app_name: str = None, guild=None):
        if not app_name is None and not guild is None:
            raise Exception("app_name and guild cannot be mixed")

        with open(self.guilds_path, encoding="utf8") as file:
            data = json.load(file)

        if app_name is None and not guild is None:
            return data[str(guild)]["apps"]

        apps: dict = {}

        for guild_id in list(data.keys()):
            for app in data[str(guild_id)]["apps"]:
                if app not in list(apps.keys()):
                    apps[app] = [discord.Object(id=int(guild_id))]

                else:
                    apps[app].append(guild_id)

        if app_name is None:
            return apps

        elif app_name in list(apps.keys()):
            return apps[app_name]

        else:
            return []

    def get_admin_guilds(self, admin_id=None, guild=None):
        if not admin_id is None and not guild is None:
            raise Exception("admin_id and guild cannot be mixed")

        with open(self.guilds_path, encoding="utf8") as file:
            data = json.load(file)

        if admin_id is None and not guild is None:
            return data[str(guild)]["admin"]

        apps: dict = {}

        for guild_id in list(data.keys()):
            for app in data[str(guild_id)]["admin"]:
                if app not in list(apps.keys()):
                    apps[app] = [discord.Object(id=int(guild_id))]

                else:
                    apps[app].append(guild_id)

        if admin_id is None:
            return apps

        elif admin_id in list(apps.keys()):
            return apps[admin_id]

        return []

    def get_theme_guilds(self, theme_color=None, guild=None):
        if not theme_color is None and not guild is None:
            raise Exception("theme_color and guild cannot be mixed")

        with open(self.guilds_path, encoding="utf8") as file:
            data = json.load(file)

        if theme_color is None and not guild is None:
            return data[str(guild)]["theme"]

        apps: dict = {}

        for guild_id in list(data.keys()):
            for app in data[str(guild_id)]["theme"]:
                if app not in list(apps.keys()):
                    apps[app] = [discord.Object(id=int(guild_id))]

                else:
                    apps[app].append(guild_id)

        if theme_color is None:
            return apps

        elif theme_color in list(apps.keys()):
            return apps[theme_color]

        return []
