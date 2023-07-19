from .types import *
from .store import App_store
from .save import Save
from .utils import Guilds, Task, LANGAGE, import_module
from .event import Event
from .com import *

from discord.ext import commands as discord_commands

from discord import Interaction
import requests_html
import json
import asyncio

class Lib_UsOS:
    """"""
    def __init__(self) -> None:
        self.app = App()
        self.app_name = ""
        self.client: discord_commands.bot = None
        self.store = App_store(None)
        self.save = Save(self.app_name)
        self.guilds = Guilds()
        self.event = Event()


    def set_app_name(self, app_name: str) -> None:
        """"""
        self.app_name = app_name
        self.save.app_name = app_name
        self.app_path = f"app/{app_name}/"
        if self.app.fusioned:
            for mod in self.app.fusioned_module:
                mod.Lib.set_app_name(app_name)

    def init(self, bot_client: discord_commands.Bot, tasks, installed_app):
        """"""
        self.client = bot_client
        self.tasks = tasks
        self.store = App_store(installed_app)
        if self.app.fusioned:
            for app in self.app.fusioned_module:
                app.Lib.init(bot_client, tasks, installed_app)

    def is_in_guild(self, ctx:discord_commands.Context):
        guild_id = ctx.guild.id
        

    def is_in_staff(self, ctx:Interaction | discord_commands.Context, direct_author=False):
        """"""
        if type(ctx) == Interaction:
            user = ctx.user
        else:
            user = ctx.author
        if user.id in self.guilds.get_admin_guilds(guild = ctx.guild_id if type(ctx)==Interaction else ctx.guild.id):
            return True

        roles = [role.name for role in user.roles]
        admins = ["Admin", "Modo", "Bot Dev"]

        for role in roles:
            if role in admins:
                return True

    def get_last_update_stats(self):
        """"""
        url = f'https://github.com/GalTechDev/UnderStar-OS/blob/master/.version'
        session = requests_html.HTMLSession()
        r = session.get(url)
        content = r.html.find('.blob-code', first=True)
        #lines = [ligne.text for ligne in content]
        return float(content.text)

    def get_lang_name(self):
        """"""
        with open("system/lang/ref.json") as file:
            data = json.load(file)
        return data

    def get_lang(self, lang = LANGAGE):
        """"""
        ref = self.get_lang_name()
        lang_txt = ref[lang]
        with open(f"system/lang/{lang_txt}.txt") as file:
            all_text = file.readlines()
        return all_text

    def get_lang_ref(self, ref, lang = LANGAGE):
        """"""
        all_ref = self.get_lang(lang)
        if type(ref) == int:
            return all_ref[ref][:-1]
        elif type(ref) == list:
            return [all_ref[one_ref][:-1] for one_ref in ref]
        else:
            raise Exception

    async def change_presence(self, activity, status):
        """"""
        await self.client.change_presence(activity=activity, status=status)
        
    def get_apps(self) -> dict:
        """"""
        return self.store.installed_app

class App:
    """"""
    def __init__(self) -> None:
        self.commands = []
        self.slashs = []
        self.all_tasks = []
        self.discord_tasks=[]
        self.help_com = None
        self.conf_com = None
        self.fusioned = False
        self.fusioned_module = []

    def command(self, name=None, help_text: str="", aliases: list=[], checks=[], force_name: bool = False):
        """"""
        def apply(funct):
            self.commands.append(Command(name if name else funct.__name__ , funct, help_text, aliases, checks, force_name))
            return funct
        return apply

    def slash(self, name: Union[str, locale_str] = None, description: Union[str, locale_str] = "No description", nsfw: bool = False, parent: Optional[Group] = None, guild_ids: Optional[List[int]] = None, auto_locale_strings: bool = True, extras: Dict[Any, Any] = ..., direct_command: bool = False):
        """"""
        def apply(funct):
            self.slashs.append(Slash(name = name.lower().replace(" ", "-") if name else funct.__name__ , description=description, callback = funct, nsfw=nsfw, parent=parent, guild_ids=guild_ids, auto_locale_strings=auto_locale_strings, extras=extras, direct_command=direct_command))
            return funct
        return apply

    def help(self):
        """"""
        def apply(funct):
            self.help_com = funct
            return funct
        return apply

    def config(self):
        """"""
        def apply(funct):
            self.conf_com = funct
            return funct
        return apply

    def loop(self,
    seconds: float = MISSING,
    minutes: float = MISSING,
    hours: float = MISSING,
    time: Union[datetime.time, Sequence[datetime.time]] = MISSING,
    count: Optional[int] = None,
    reconnect: bool = True,):
        """"""
        def apply(funct):
            self.all_tasks.append(Task(function=asyncio.coroutine(funct), seconds=seconds, minutes=minutes, hours=hours, count=count, time=time, reconnect=reconnect))
            return funct
        return apply

    def fusion(self, apps):
        """"""
        self.fusioned = True
        self.fusioned_module+=apps
        for app in apps:
            self.commands+=app.Lib.app.commands
            self.slashs+=app.Lib.app.slashs
            self.help_com = app.Lib.app.help_com