import discord
from discord.ext import tasks
import json


langage= "Francais"

class Command:
    def __init__(self, name:str, command, help_text: str="",aliases: (list[str])=[],checks=[]) -> None:
        self.name=name.replace(" ", "-")
        self.command=command
        self.help=help_text
        self.aliases=aliases
        self.checks=checks

class Task:
    def __init__(self,fonction,seconds: int = tasks.MISSING, minutes: int = tasks.MISSING, hours: int = tasks.MISSING, time=tasks.MISSING, count = None, reconnect: bool = True) -> None:
        self.fonction=fonction
        self.seconds=seconds
        self.minutes=minutes
        self.hours=hours
        self.count=count
        self.reconnect=reconnect
        self.time=time

def is_in_staff(ctx, direct_author=False):
    if ctx.author.id in [608779421683417144]:
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
