# coding: utf-8
from itertools import cycle
from pathlib import Path
import discord
from discord.ext import commands, tasks
import os.path
import time
import sys
import save.system.installed_app as apps
import system.sys_app as sys_apps
import asyncio
from system.lib import *

Lib = Lib_UsOS()




bot_version = "0.1"
sys_folder = "system"
token_folder = "token"
save_folder = "save"
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

def get_apps(sys=False) -> dict:
    return sys_apps.all_app if sys else apps.all_app

async def import_apps(sys=False):
    for app_name,app in get_apps(sys).items():
        print(f"\nIMPORT {app_name}: ")
        loaded = 0
        errors = 0
        error_lst=[]

        app.Lib.init_client(client)
        app.Lib.set_app_name(app_name)
        
        for command in app.Lib.app.commands:
            try:
                new_com=commands.Command(command.command,name=f"{app_name}-{command.name}" if not command.force_name else command.name,help=command.help,aliases=command.aliases,checks=command.checks)
                if not new_com in client.all_commands.keys():
                    client.add_command(new_com)
                    loaded+=1
            except Exception as error:
                errors+=1
                error_lst.append(error)
        print(f"Command : {loaded} loaded | {errors} error : {error_lst}")
            
        for task in app.Lib.app.task:
            new_task=tasks.Loop(task.fonction,seconds=task.seconds, hours=task.hours,minutes=task.minutes, time=task.time, count=task.count, reconnect=task.reconnect)
            #await new_task.start()

        loaded = 0
        errors = 0
        error_lst=[] 

        for command in app.Lib.app.slashs:
            try:
                #new_com=commands.Command(command.command,name=f"{app_name}-{command.name}",help=command.help,aliases=command.aliases,checks=command.checks)
                new_com=discord.app_commands.Command(name=f"{app_name.lower()}-{command.name.lower()}" if not command.force_name else command.name, description=command.description,callback=command.command)
                new_com.guild_only = True
                #new_com.default_permissions=discord.Permissions(8)
                if not new_com.name in [com.name for com in client.tree._get_all_commands()]:
                    client.tree.add_command(new_com, guild=command.guild, guilds=command.guilds)
                    loaded+=1
            except Exception as error:
                errors+=1
                error_lst.append(error)
            
        print(f"Slash : {loaded} loaded | {errors} error : {error_lst}")


def get_help(ctx:commands.context.Context):
    embeds = []
    embed = discord.Embed(title="OS Commands", description=f"Préfix : `{prefix}` | Version : `{bot_version}`", color=discord.Color.red())
    try:
        coms = [com for com in client.all_commands]
        coms.sort()
        nb = 0
        page = 1
        nb_page = len(coms)//25
        embed.set_author(name=f'Liste des commandes {(page+"/"+nb_page) if nb_page > 1 else ""}')
        for com in coms:
            #print(com)
            if all([check(ctx) for check in client.all_commands[com].checks]+[True]):
                embed.add_field(name=f"**{com}**", value=f'{client.all_commands[com].help if client.all_commands[com].help != None else "Aucune aide disponible"}')
                nb+=1
            if nb==25:
                nb=0
                embeds.append(embed.copy())
                embed = discord.Embed(title="OS Commands", color=discord.Color.red())
                embed.set_author(name=f'Liste des commandes {page}/{nb_page}')
                page+=1
    except Exception as error:
        print(error)

    return embeds


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

# -------------------------------- Slash Command -------------------

@client.tree.command(name = "info", description = "Donne des infos sur le bot", guild=None) #, guilds=[discord.Object(id=649021344058441739)] Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@discord.app_commands.check(Lib.is_in_staff)
async def info(ctx:discord.Interaction):
    embed = discord.Embed(title="INFO")
    embed.add_field(name=f"Version :", value=f"` {bot_version}   `")
    embed.add_field(name=f"Ping :", value=f"` {round(client.latency * 1000)} `")
    embed.add_field(name=f"Time up :", value=f"`{convert_time(int(time.time()-timer))}`")
    await ctx.response.send_message(embed=embed, ephemeral=True)


# -------------------------------- COMMANDE -------------------------------

@client.command(name="os-test", help="Envoie une pizza gatuite")
async def test(ctx:commands.context.Context):
    await ctx.send(":pizza:")


@client.command(name="os-ping", aliases=["os-ver", "ver", "ping"], help="Donne des infos sur le bot")
@commands.check(Lib.is_in_staff)
async def version(ctx:commands.context.Context):
    embed = discord.Embed(title="INFO")
    embed.add_field(name=f"Version :", value=f"` {bot_version}   `")
    embed.add_field(name=f"Ping :", value=f"` {round(client.latency * 1000)} `")
    embed.add_field(name=f"Time up :", value=f"`{convert_time(int(time.time()-timer))}`")
    await ctx.send(embed=embed)


@client.command(name="os-help", aliases=["help"], help="Pour avoir ce message")
async def help(ctx:commands.context.Context,*args):
    if args==():
        await ctx.send(embeds=get_help(ctx))
    else :
        if args[0] in get_apps().keys():
            sys_com = False
        elif args[0] in get_apps(True).keys():
            sys_com = True
        if len(args)==1:
            try:
                await get_apps(sys_com)[args[0]].Lib.help(ctx)
            except Exception as error:
                if type(error) == AttributeError:
                    await ctx.send(content=f"L'application `{args[0]}` n'a pas de fonction d'aide")
                else:
                    await ctx.send(content=f"La fonction d'aide de l'application `{args[0]}` ne fonctionne pas. Merci de contacter son développeur.")
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
    #maintenance.start()

    with open(f'{sys_folder}/icon.png', 'rb') as image:
        pass
        #await client.user.edit(avatar=image.read())

    print("version : ", programmer, bot_version)
    print("Logged in as : ", client.user.name)
    print("ID : ", client.user.id)
    await import_apps(True)
    await import_apps()
    
    for guild in client.guilds:
        pass
        if "sync" in sys.argv:
            client.tree.copy_global_to(guild=discord.Object(id=guild.id))
        await client.tree.sync(guild=discord.Object(id=guild.id))
        await client.tree.sync()
    if "sync" in sys.argv:
        os.execv(sys.executable, ["None", os.path.basename(sys.argv[0])])

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
    print("error h", error)

@client.tree.error
async def on_app_command_error(ctx: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CheckFailure):
        await ctx.response.send_message('Tu ne remplis pas les conditions pour executer cette commande.', ephemeral=True)
    elif isinstance(error, discord.app_commands.BotMissingPermissions):
        await ctx.response.send_message('Le bot ne peut pas executer cette commande car il lui manque des autorisations. Merci de contacter le STAFF', ephemeral=True)

# ----------------------------COMMANDE MAINTENANCE----------------------------------


@client.command(name="re", help="Pour restart le bot")
@commands.check(Lib.is_in_staff)
async def reboot(ctx:commands.context.Context):
    await client.change_presence(activity=discord.Game("Restarting..."), status=discord.Status.dnd)

    await ctx.send("Restarting bot")
    os.execv(sys.executable, ["None", os.path.basename(sys.argv[0])])


@client.command(help="stop le bot")
@commands.check(Lib.is_in_staff)
async def stop(ctx:commands.context.Context):
    await ctx.send("Stopping")
    await client.change_presence(activity=discord.Game("Shutting down..."), status=discord.Status.dnd)
    exit(1)
    quit()


@client.command(aliases=["upt"], help="Pour update le bot")
@commands.check(is_dev)
async def update(ctx:commands.context.Context, *, ipe=programmer):
    await ctx.send("updating code !")
    await client.change_presence(activity=discord.Game("Updating..."), status=discord.Status.idle)

    val = os.system(f"start {update_file}")

    await client.change_presence(activity=discord.Game("Back from updt !"), status=discord.Status.online)
    print(val)
    if val==0:
        await ctx.send("Done")
        await client.close()
    else:
        await ctx.send("Error!")
        exit(0)


# -------------------------------------- TASKS -----------------------------------


@tasks.loop(seconds=127)
async def change_status():
    if "sync" in sys.argv:
        await client.change_presence(activity=discord.Game("Re-Sync..."), status=discord.Status.dnd)
    else:
        await client.change_presence(activity=discord.Game(next(status)))

"""
resetSystem = False


@tasks.loop(seconds=43201)
async def maintenance():
    global resetSystem
    if resetSystem:
        await client.change_presence(activity=discord.Game("Restarting..."), status=discord.Status.idle)
        os.execv(sys.executable, ["None", os.path.basename(sys.argv[0])])

    resetSystem = True
"""
client.run(bot_token)
