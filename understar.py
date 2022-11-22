# coding: utf-8
from itertools import cycle
from pathlib import Path
import discord
from discord.ext import commands, tasks
import os.path
import time
import sys
import system.installed_app as apps
import asyncio

bot_version = "0.1"
sys_folder = "system"
token_folder = "token"
app_folder = "app"
classbot_token = f"{token_folder}/classbot_token"
update_file = f"{sys_folder}/app/update/update.pyw"
prefix="?"

programmer = os.path.basename(sys.argv[0])


vals = [sys_folder,app_folder]

for name in vals:
    Path(name).mkdir(exist_ok=True)

bot_token = ""

try:
    with open(classbot_token, "r") as f:
        bot_token = f.readlines()[0].strip()
except FileNotFoundError:
    with open(classbot_token, "w") as f:
        f.write("TOKEN_HERE")
        input("please insert the bot token in the file classbot_token")
        sys.exit(0)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix=prefix, help_command=None)
client.remove_command('help')



status = cycle(["UnderStar OS"])

def get_apps() -> dict:
    return apps.all_app

async def import_apps():
    import system.installed_app as apps
    for app_name,app in get_apps().items():
        app.__init__(client)
        for command in app.commands:
            new_com=commands.Command(command.command,name=f"{app_name}-{command.name}",help=command.help,aliases=command.aliases,checks=command.checks)
            if not new_com in client.all_commands.keys():
                client.add_command(new_com)
        
        for task in app.task:
            new_task=tasks.Loop(task.fonction,seconds=task.seconds, hours=task.hours,minutes=task.minutes, time=task.time, count=task.count, reconnect=task.reconnect)
            #await new_task.start()
        
        for command in app.slashs:
            #new_com=commands.Command(command.command,name=f"{app_name}-{command.name}",help=command.help,aliases=command.aliases,checks=command.checks)
            new_com=discord.app_commands.Command(name=f"{app_name}-{command.name}", description=command.description,callback=command.command)
            new_com.default_permissions=discord.Permissions(8)
            if not new_com in client.tree._get_all_commands():
                client.tree.add_command(new_com, guild=command.guild, guilds=command.guilds)
                
        
            


def get_help(ctx, is_slash: bool = False):
    embed = discord.Embed(title="OS Commands", description=f"Préfix : `{prefix}`", color=discord.Color.red())
    embed.set_author(name='Liste des commandes')
    if is_in_staff(ctx):
        embed.add_field(name="**help**", value="pour avoir ce message")
        embed.add_field(name="**reboot**", value="pour restart le bot")
        embed.add_field(name="**stop**", value="stop le bot")
        embed.add_field(name="**version**", value="donne la version du bot")

    return embed


def convert_time(value: int):
    val3, val2, val = 0, value//60, value % 60
    message = f"{val2}min {val}s."

    if val2 > 60:
        val3, val2 = val2//60, val2 % 60
        message = f"{val3}h {val2}min {val}s."

    return message


def is_dev(ctx):
    if ctx.author.id in [608779421683417144]:
        return True

    member = ctx.message.author
    roles = [role.name for role in member.roles]
    admins = ["Bot Dev"]

    for role in roles:
        if role in admins:
            return True


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


def is_in_maintenance(ctx):
    if ctx.author.id in [366055261930127360, 649532920599543828]:
        return True

    member = ctx.message.author
    roles = [role.name for role in member.roles]
    admins = ["Admin", "Modo", "Bot Dev"]

    for role in roles:
        if role in admins:
            return True

        if "maint." in role:
            return True

timer = time.time()

# -------------------------------- Slash Command (test) -------------------

@client.tree.command(name = "commandtest", description = "Command test", guilds=[discord.Object(id=649021344058441739)]) # Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    await interaction.response.send_message("Hello!")




# -------------------------------- COMMANDE -------------------------------

@client.command(name="os-test")
async def test(ctx):
    await ctx.send(":pizza:")
   


@client.command(name="os-ping", aliases=["os-ver"])
@commands.check(is_in_staff)
async def version(ctx:commands.context.Context):
    value = int(time.time()-timer)
    message = convert_time(value)
    final_message = f"version : {bot_version}\nping : {round(client.latency * 1000)}ms :ping_pong:\ntime up : {message}"
    await ctx.send(final_message)


@client.command(name="os-clear", aliases=["clear"])
@commands.cooldown(1, 300, commands.BucketType.user)
async def clear(ctx:commands.context.Context, amount=1):
    if is_in_staff(ctx):
        await ctx.channel.purge(limit=amount+1)
        clear.reset_cooldown(ctx)
    elif amount < 5:
        await ctx.channel.purge(limit=amount+1)
    else:
        await ctx.channel.purge(limit=6)


@client.command(name="os-help", aliases=["help"])
async def help(ctx:commands.context.Context,*args):
    print(args)
    if args==():
        await ctx.send(embed=get_help(ctx, False))
    elif args[0] in get_apps().keys():
        if len(args)==1:
            await get_apps()[args[0]].help(ctx)
        else:
            if f"{args[0]}-{args[1]}" in client.all_commands.keys():
                embed = discord.Embed(title=f"Aide sur la commande `{args[1]}`", description=f"Commande : `{prefix}{args[0]}-{args[1]}`", color=discord.Color.red())
                embed.set_author(name=f'App : {args[0]}')
                aide=client.all_commands[f"{args[0]}-{args[1]}"].help if client.all_commands[f"{args[0]}-{args[1]}"].help!="" else "Pas d'aide pour cette commande"
                alias=""
                for command in client.all_commands.keys():
                    if command!=f"{args[0]}-{args[1]}" and client.all_commands[command]==client.all_commands[f"{args[0]}-{args[1]}"]:
                        alias+=f"{command}, "
                embed.add_field(name=f"**{aide}**", value=f"Alias : {alias[:-1]}")
            else:
                embed = discord.Embed(title=f"La Command `{args[1]}` n'existe pas", description=f"Préfix de l'app : `{prefix}{args[0]}-`", color=discord.Color.red())
                embed.set_author(name=f"App : {args[0]}")
                #embed.add_field(name=f"**La Command {args[1]} n'existe pas**", value=f"Commande d'aide de l'application {args[0]} : !{args[0]}-help")
            try:
                await ctx.send(embed=embed)
            except Exception as error:
                print(error)

# ---------------------------------- EVENTS ------------------------------------
@client.event
async def on_ready():
    change_status.start()
    maintenance.start()

    with open(f'{sys_folder}/icon.png', 'rb') as image:
        pass
        #await client.user.edit(avatar=image.read())

    print("version : ", programmer, bot_version)
    print("Logged in as : ", client.user.name)
    print("ID : ", client.user.id)
    await import_apps()
    for guild in client.guilds:
        await client.tree.sync(guild=discord.Object(id=guild.id))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments')

    elif isinstance(error, commands.CommandOnCooldown):
        value = int(f"{error.retry_after:.0f}")
        message = "Try again in "
        message += convert_time(value)

        em = discord.Embed(title="Slow it down bro!", description=message)
        await ctx.send(embed=em)

# ----------------------------COMMANDE MAINTENANCE----------------------------------


@client.command()
@commands.check(is_in_staff)
async def reboot(ctx:commands.context.Context):
    await client.change_presence(activity=discord.Game("Restarting..."), status=discord.Status.dnd)

    await ctx.send("Restarting bot")
    os.execv(sys.executable, ["None", os.path.basename(sys.argv[0])])


@client.command()
@commands.check(is_in_staff)
async def stop(ctx:commands.context.Context):
    await ctx.send("Stopping")
    await client.change_presence(activity=discord.Game("Shutting down..."), status=discord.Status.dnd)
    exit(1)
    quit()


@client.command(aliases=["upt"])
@commands.check(is_dev)
async def update(ctx:commands.context.Context, *, ipe=programmer):
    await ctx.send("updating code !")
    await client.change_presence(activity=discord.Game("Updating..."), status=discord.Status.idle)

    val = os.system(f"start {update_file}")

    await client.change_presence(activity=discord.Game("Back from updt !"), status=discord.Status.online)
    print(val)
    if val==1:
        await ctx.send("Done")
        await client.close()
    else:
        await ctx.send("Error!")
        exit(0)


# -------------------------------------- TASKS -----------------------------------


@tasks.loop(seconds=127)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


resetSystem = False


@tasks.loop(seconds=43201)
async def maintenance():
    global resetSystem
    if resetSystem:
        await client.change_presence(activity=discord.Game("Restarting..."), status=discord.Status.idle)
        os.execv(sys.executable, ["None", os.path.basename(sys.argv[0])])

    resetSystem = True

client.run(bot_token)
