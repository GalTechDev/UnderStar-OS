class Command:
    def __init__(self, name:str, command, help_text: str="",aliases: (list[str])=[],checks=[]) -> None:
        self.name=name.replace(" ", "-")
        self.command=command
        self.help=help_text
        self.aliases=aliases
        self.checks=checks

class Task:
    def __init__(self,fonction,seconds: int = 0, minutes: int = 0, hours: int = 0, count = None, reconnect: bool = True, loop= None) -> None:
        self.fonction=fonction
        self.seconds=seconds
        self.minutes=minutes
        self.hours=hours
        self.count=count
        self.reconnect=reconnect
        self.loop=loop

def is_in_staff(ctx, direct_author=False):
    if ctx.author.id in []:
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