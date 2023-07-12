from .types import *
from discord.app_commands import Command, locale_str, Group

class Slash(Command):
    """"""
    def __init__(self, *, name: Union[str, locale_str], description: Union[str, locale_str], callback, nsfw: bool = False, parent: Optional[Group] = None, guild_ids: Optional[List[int]] = None, auto_locale_strings: bool = True, extras: Dict[Any, Any] = ..., direct_command = False):
        super().__init__(name=name, description=description, callback=callback, nsfw=nsfw, parent=parent, guild_ids=guild_ids, auto_locale_strings=auto_locale_strings, extras=extras)
        self.direct_command = direct_command

class Command:
    """"""
    def __init__(self, name:str, command, help_text: str="",aliases: list=[],checks=[], force_name: bool = False) -> None:
        self.name=name.replace(" ", "-")
        self.command=command
        self.help = help_text if help_text!="" else "Aucune aide disponible"
        self.aliases=aliases
        self.checks=checks
        self.force_name = force_name