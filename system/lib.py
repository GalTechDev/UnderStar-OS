import discord
from discord.ext import tasks as discord_tasks
import json


langage= "Francais"

commands = []
slashs = []
task = []


class Slash:
    def __init__(self, name: str, description: str, command, guild = discord.app_commands.tree.MISSING, guilds: list = discord.app_commands.tree.MISSING) -> None:
        self.name=name.replace(" ", "-")
        self.command=command
        self.description=description
        self.guild=guild
        self.guilds=guilds
        

class Command:
    def __init__(self, name:str, command, help_text: str="",aliases: (list[str])=[],checks=[]) -> None:
        self.name=name.replace(" ", "-")
        self.command=command
        self.help=help_text
        self.aliases=aliases
        self.checks=checks

class Task:
    def __init__(self,fonction,seconds: int = discord_tasks.MISSING, minutes: int = discord_tasks.MISSING, hours: int = discord_tasks.MISSING, time=discord_tasks.MISSING, count = None, reconnect: bool = True) -> None:
        self.fonction=fonction
        self.seconds=seconds
        self.minutes=minutes
        self.hours=hours
        self.count=count
        self.reconnect=reconnect
        self.time=time

def command(name=None, help_text: str="", aliases: (list[str])=[], checks=[]):
    def apply(funct):
        commands.append(Command(name if name != None else funct.__name__ , funct, help_text, aliases, checks))
        return funct
    return apply

def slash(description: str, name: str = None, guild = discord.utils.MISSING, guilds: list = discord.utils.MISSING):
    def apply(funct):
        slashs.append(Slash(name if name != None else funct.__name__ , description, funct, guild, guilds))
        return funct
    return apply

def tasks(seconds: int = discord_tasks.MISSING, minutes: int = discord_tasks.MISSING, hours: int = discord_tasks.MISSING, time=discord_tasks.MISSING, count = None, reconnect: bool = True):
    def apply(funct):
        task.append(Task(funct, seconds, minutes, hours, time, count, reconnect))
        return funct
    return apply


def is_in_staff(ctx:discord.Interaction, direct_author=False):
    if not direct_author:
        member = ctx.author
    else:
        member = ctx.user
    if member.id in [608779421683417144]:
        return True
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


