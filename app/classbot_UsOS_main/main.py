# coding: utf-8
from pdf2image import convert_from_path
from datetime import datetime, date
from app.classbot_UsOS_main.RoleManager import RoleManager
from pathlib import Path
import asyncio
import requests
import os.path
import json
import time
import sys
import system.lib  as lib

discord = lib.discord
Lib = lib.Lib_UsOS()

app_version = "4.0.0"
app_folder = "app/classbot_UsOS_main"
classbot_folder = f"{app_folder}/classbot_folder"
classbot_config_file = f"{classbot_folder}/classbot_config.json"
role_folder = f"{classbot_folder}/role_database.json"

edt_database_path = f"{classbot_folder}/edt_database.json"
edt_path = f"{app_folder}/pdf"

programmer = os.path.basename(sys.argv[0])
role_db = RoleManager(role_folder)

vals = [classbot_folder, edt_path]

for name in vals:
    Path(name).mkdir(exist_ok=True)

launch_check_edt = True

def __init__(bot_client):
    global client
    client=bot_client
    init_event()

def get_config():
    return {"edt": launch_check_edt}


try:
    with open(classbot_config_file, "rb") as f:
        bot_config = json.loads(f.read())
        launch_check_edt = bot_config["edt"]
        # launch_check_edt = True

except (FileNotFoundError, KeyError):
    with open(classbot_config_file, "w") as f:
        f.write(json.dumps(get_config(), indent=4))


current_semester = "infoS1"
try:
    with open(edt_database_path, "rb") as f:
        liscInfo = json.loads(f.read())[current_semester]

except (FileNotFoundError, KeyError):
    pass


intents = discord.Intents.default()
intents.members = True



def convert_time(value: int):
    val3, val2, val = 0, value//60, value % 60
    message = f"{val2}min {val}s."

    if val2 > 60:
        val3, val2 = val2//60, val2 % 60
        message = f"{val3}h {val2}min {val}s."

    return message


def update_edt_database(key, value):
    global liscInfo
    with open(edt_database_path, "rb") as f:
        database = json.loads(f.read())

    val = database[current_semester].get(key)

    if not val:
        return False

    try:
        database[current_semester][key] = value
    except Exception:
        return False

    with open(edt_database_path, "w") as f:
        f.write(json.dumps(database, indent=4))

    liscInfo = database[current_semester]
    return True


def convert_url(url: str = ""):
    if "edtweb2" not in url:
        return False

    current_date = date.isocalendar(datetime.now())
    num_semaine = current_date[1]

    if current_date[2] > 5:
        num_semaine += 1

    temp_url = url.split("edtweb2")[1:].pop(0)
    temp_url = temp_url.split("/")[1:]

    magic = temp_url.pop(0).split(".")
    magic2 = temp_url[0].replace("PDF_EDT_", "")
    magic2 = magic2.split(".pdf")[0].split("_")

    id0 = int(magic.pop(0))
    id1 = int(magic2.pop(0))

    chiffre_temporaire = int(magic2[0])

    temp = int(magic[0])

    if num_semaine - chiffre_temporaire < 0:
        return False

    id2 = chiffre_temporaire - temp

    value = [id0, id1, id2]

    infos = check_edt_info(value)

    try:
        size = int(infos["Content-Length"])
    except KeyError:
        size = 0
    status = int(infos["status"])

    if size < 500 or status != 200:
        return False

    return value


def is_it_me(ctx):
    if ctx.author.id in (366055261930127360, 649532920599543828):
        return True


def is_dev(ctx):
    if ctx.author.id in (366055261930127360, 649532920599543828):
        return True

    member = ctx.message.author
    roles = [role.name for role in member.roles]
    admins = ["Bot Dev"]

    for role in roles:
        if role in admins:
            return True

def is_in_maintenance(ctx):
    if ctx.author.id in (366055261930127360, 649532920599543828):
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

async def binaire(ctx, message):
    message = "Error!"
    try:
        message = f"Binaire : {bin(int(message))[2:]}\nEntier : {int(message, 2)}"
    except ValueError:
        message = f"Entier : {int(message, 2)}"

    await ctx.send(message)

@Lib.app.slash(name="sedt", description="Switch auto edt update on/off")
@Lib.app.command(name="sedt", aliases=["sedt"], help_text="Switch auto edt update on/off")
async def sedt(ctx:discord.Interaction):
    global launch_check_edt

    val = True
    if launch_check_edt:
        val = False

    launch_check_edt = val

    with open(classbot_config_file, "w") as f:
        f.write(json.dumps(get_config(), indent=4))

    await ctx.channel.send(f"check edt set on : {val}")

@Lib.app.command(name="uptedt", aliases=["uptedt"], checks=[Lib.is_in_staff])
async def uptedt(ctx, url: str, cle_dico: str = ""):
    gestion = "maint."
    val = convert_url(url)
    print(val)

    if not val:
        await ctx.send("`Error! Something went wrong with the url!`")
        return

    member = ctx.message.author
    roles = [role.name for role in member.roles]

    if "Admin" not in roles:
        for role in roles:
            if gestion not in role:
                continue

            role = role.lower().replace(gestion, "").replace(" ", "")

            if role in liscInfo.keys():
                cle_dico = role
                break

    if not cle_dico:
        await ctx.send("`Error! Something went wrong with the role!`")
        return

    check = update_edt_database(cle_dico, val)

    if not check:
        await ctx.send("`Error! Something went wrong with the role!`")
        return

    await ctx.send("`EDT database successfully updated!`")


async def getdb(ctx):
    with open(edt_database_path, 'rb') as fp:
        await ctx.send(file=discord.File(fp, "edt_database.json"))


async def pushdb(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Error! No file attached!")
        return

    attachment = ctx.message.attachments[0].url
    name = ctx.message.attachments[0].filename

    if name.lower() != "edt_database.json":
        await ctx.send("Error! Not a valid filename!")
        return

    with requests.get(attachment, stream=True) as r:
        with open(edt_database_path, 'wb') as fd:
            for chunk in r.iter_content(1000):
                fd.write(chunk)

    await ctx.send(f"File installed at : {edt_database_path}")

@Lib.app.slash(name="edt", description="Envoie ton emploi du temps", guild=discord.Object(id=649021344058441739))
async def edt(ctx:discord.Interaction, cle_dico:str="", plus:int=0):
    #plus = plus.replace("+", "")

    if cle_dico not in liscInfo.keys():
        cle_dico = cle_dico.replace("+", "")
        #plus = cle_dico
        cle_dico = ""

    if not cle_dico:
        member = ctx.user
        roles = [role.name for role in member.roles]
        for role in roles:
            role = role.lower().replace(" ", "")
            if role in liscInfo.keys():
                cle_dico = role
                break

    pdf_name = f"ask-{cle_dico}.pdf"

    try:
        plus = int(plus)
    except Exception:
        plus = 0

    corrupt = False
    
    infos = check_edt_info(liscInfo[cle_dico], plus)

    try:
        size = int(infos["Content-Length"])
    except KeyError:
        size = 0

    status = int(infos["status"])

    if (size < 500) or (status != 200):
        pdf_name = f"{cle_dico}.pdf"
        corrupt = True
    else:
        download_edt(pdf_name, liscInfo[cle_dico], plus)

    channel = ctx.channel

    message = f"EDT pour : {cle_dico.upper()}"
    if plus:
        message += f' ({"+" if plus >0 else ""}{plus})'

    current_date = date.isocalendar(datetime.now())

    week_end = False
    if current_date[2] > 5:
        week_end = True

    if corrupt and week_end:
        await channel.send(f"\nURL générée invalide, voir sur le site, en attendant un Admin\n`Ceci est une ancienne version!`")
        # await channel.send("`URL générée invalide, contactez un Admin pour de l'aide`")
        return

    elif corrupt:
        message += f"\nURL générée invalide, voir sur le site, en attendant un Admin\n`Ceci est une ancienne version!`"
        # message += "\n`EDT Corrompu! Ceci est une ancienne version!`"

    
    await send_edt_to_chat(ctx, message, pdf_name, liscInfo[cle_dico])


async def addrole(ctx, role_: discord.Role, emote): #aliases=["addmention", "addemoji", "addemote"]
    try:
        refId = ctx.message.reference.message_id
    except Exception:
        await ctx.channel.send("Erreur! Pas de message lié!")
        return

    try:
        role = role_.name
    except Exception:
        await ctx.channel.send("Erreur! Role inexistant")
        return

    emote = emote

    commu = ctx.guild.id
    chat = ctx.channel.id

    guild_info = client.get_guild(int(commu))
    channel = guild_info.get_channel(int(chat))
    role_message = await channel.fetch_message(int(refId))

    try:
        await role_message.add_reaction(emote)
    except Exception:
        await ctx.channel.send("Erreur! Mauvaise emote!")
        return

    await role_db.bind(commu, chat, refId, emote, role)
    role_db.save(role_db.role_database)

    channel = guild_info.get_channel(int(chat))
    role_message = await channel.fetch_message(ctx.message.id)
    await role_message.add_reaction("✅")
    await ctx.channel.purge(limit=1)


async def removerole(ctx, role: discord.Role):

    try:
        refId = ctx.message.reference.message_id
    except Exception:
        await ctx.channel.send("Erreur! Pas de message lié!")
        return

    role_name = role.name
    commu = ctx.guild.id
    chat = ctx.channel.id

    guild_info = client.get_guild(int(commu))

    try:
        role_db.remove_role(commu, chat, refId, role_name)
    except Exception:
        await ctx.channel.send("Erreur! Role inexistant")
        return

    role_db.save(role_db.role_database)

    channel = guild_info.get_channel(int(chat))
    role_message = await channel.fetch_message(ctx.message.id)
    await role_message.add_reaction("✅")
    await ctx.channel.purge(limit=1)


async def removeemote(ctx, emote):

    try:
        refId = ctx.message.reference.message_id
    except Exception:
        await ctx.channel.send("Erreur! Pas de message lié!")
        return

    role_name = emote
    commu = ctx.guild.id
    chat = ctx.channel.id

    guild_info = client.get_guild(int(commu))

    try:
        role_db.remove_emote(commu, chat, refId, role_name)
    except Exception:
        await ctx.channel.send("Erreur! Emote inexistant")
        return

    role_db.save(role_db.role_database)

    channel = guild_info.get_channel(int(chat))
    role_message = await channel.fetch_message(ctx.message.id)
    await role_message.add_reaction("✅")
    await ctx.channel.purge(limit=1)


# -------------------------------- SLASH COMMANDE -------------------------------


@Lib.app.slash(name="addrole", description="liste des commande", guild=discord.Object(id=649021344058441739))
async def addrole_slash(ctx: discord.Interaction, role: discord.Role, emote: str, message_id: int):
    if not Lib.is_in_staff(ctx, True):
        await ctx.response.send_message(content="Vous n'avez pas les permissions pour utiliser cette commande.", ephemeral=True)
        return

    refId = message_id
    role = role.name
    commu = ctx.guild.id
    chat = ctx.channel.id

    guild_info = client.get_guild(int(commu))
    channel = guild_info.get_channel(int(chat))
    message = ""
    try:
        role_message = await channel.fetch_message(int(refId))
        try:
            await role_message.add_reaction(emote)
        except Exception:
            message+="Erreur! Mauvaise emote!\n"
    except Exception:
        message+="Erreur! message_id invalide!\n"
    finally:
        if message != "":
            await ctx.response.send_message(message, ephemeral=True)
            return

    await role_db.bind(commu, chat, refId, emote, role)
    role_db.save(role_db.role_database)
    await ctx.response.send_message(f"{role} à bien été créé avec l'emote {emote}.", ephemeral=True)


@Lib.app.slash(name="removerole", description="retire le role", guild=discord.Object(id=649021344058441739))
async def removerole_slash(ctx: discord.Interaction, role: discord.Role, message_id:int):
    if not Lib.is_in_staff(ctx, True):
        await ctx.response.send_message("Vous n'avez pas les permissions pour utiliser cette commande.", ephemeral=True)
        return

    refId = message_id
    role_name = role.name
    commu = ctx.guild.id
    chat = ctx.channel.id
    guild_info = client.get_guild(int(commu))
    channel = guild_info.get_channel(int(chat))

    try:
        role_message = await channel.fetch_message(int(refId))
    except Exception:
        await ctx.response.send_message("Erreur! message_id invalide!", ephemeral=True)

    try:
        role_db.remove_role(commu, chat, refId, role_name)
    except Exception:
        await ctx.response.send_message("Erreur! Role inexistant", ephemeral=True)
        return

    role_db.save(role_db.role_database)
    await ctx.response.send_message(f"{role} à bien été retiré du message.", ephemeral=True)


@Lib.app.slash(name="removeemote", description="retir l'emote", guild=discord.Object(id=649021344058441739))
async def removeemote_slash(ctx: discord.Interaction, emote: str, message_id: int):
    if not Lib.is_in_staff(ctx, True):
        await ctx.send("Vous n'avez pas les permissions pour utiliser cette commande.", ephemeral=True)
        return

    refId = message_id
    role_name = emote
    commu = ctx.guild.id
    chat = ctx.channel.id
    guild_info = client.get_guild(int(commu))
    channel = guild_info.get_channel(int(chat))

    try:
        role_message = await channel.fetch_message(int(refId))
    except Exception:
        await ctx.response.send_message("Erreur! message_id invalide!", ephemeral=True)

    try:
        await role_message.clear_reaction(emote)
        role_db.remove_emote(commu, chat, refId, role_name)
    except Exception:
        await ctx.response.send_message("Erreur! Emote inexistant", ephemeral=True)
        return

    role_db.save(role_db.role_database)
    await ctx.response.send_message(f"{emote} à bien été retiré du message.", ephemeral=True)


async def edtpush(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Error! No file attached!")
        return

    attachment = ctx.message.attachments[0].url
    name = ctx.message.attachments[0].filename

    if name.lower() in ["liste_de_fichiers"]:
        await ctx.send("Error! Forbidden files!")
        return

    with requests.get(attachment, stream=True) as r:
        pat = f"{edt_path}/{name}"
        with open(pat, 'wb') as fd:
            for chunk in r.iter_content(1000):
                fd.write(chunk)

    await ctx.send(f"File installed at : {pat}")

# ---------------------------------- EVENTS ------------------------------------

def init_event():
    @client.event
    async def on_raw_reaction_add(ctx):
        if ctx.user_id == client.user.id:
            return

        message_id = str(ctx.message_id)
        chat_id = ctx.channel_id
        guild_id = ctx.guild_id
        # print(ctx.emoji.name)

        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        user = await guild.fetch_member(ctx.user_id)

        val = role_db.is_binded_from_emote(guild_id, chat_id, message_id, ctx.emoji.name)

        if val:
            role = discord.utils.get(guild.roles, name=val)
            await user.add_roles(role)


    @client.event
    async def on_raw_reaction_remove(ctx):
        if ctx.user_id == client.user.id:
            return

        guild_id = ctx.guild_id

        # guild_id = 550450730192994306
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)
        user = await guild.fetch_member(ctx.user_id)

        val = role_db.is_binded_from_emote(guild_id, ctx.channel_id, ctx.message_id, ctx.emoji.name)

        if val:
            role = discord.utils.get(guild.roles, name=val)
            await user.remove_roles(role)


# ----------------------------------- EDT ----------------------------------


def compare_edt(pdf_name, indices: list = None, plus: int = 0):
    path_to_pdf = f"{edt_path}/{pdf_name}"

    try:
        poid_old = os.path.getsize(path_to_pdf)
    except Exception:
        poid_old = 0

    infos = check_edt_info(indices, plus)

    try:
        poid_new = int(infos["Content-Length"])
    except KeyError:
        return 5

    # status = infos["status"]

    if poid_old == poid_new and poid_new < 500:
        # même taille et corrompu
        return 5

    elif poid_old == poid_new and poid_new < 2000:
        # même taille et erreur serveur
        return 6

    elif poid_old == poid_new:
        # même taille
        return 2

    elif poid_new < 500:
        # pdf corrompu
        return 3

    elif poid_new < 2000:
        # erreur serveur
        return 4

    return 0


def download_edt(pdf_name: str, indices: list = None, plus: int = 0):
    # permet de transfomer la date en compteur du jour dans la semaine
    # et de la semaine dans l'année (retourne l'année, le numéro de semaine et le numéro du jour)
    # utilisé pour les ids du liens pour l'edt
    current_date = date.isocalendar(datetime.now())

    num_semaine = current_date[1]
    annee = current_date[0]

    if current_date[2] > 5:
        num_semaine += 1

    while num_semaine-indices[2] < 0:
        num_semaine += 1

    url_edt = "http://applis.univ-nc.nc/gedfs/edtweb2/{}.{}/PDF_EDT_{}_{}_{}.pdf"
    url = url_edt.format(indices[0], num_semaine - indices[2] + plus, indices[1], num_semaine + plus, annee)

    path_to_pdf = f"{edt_path}/{pdf_name}"
    with requests.get(url, stream=True) as r:
        with open(path_to_pdf, 'wb') as fd:
            for chunk in r.iter_content(1000):
                fd.write(chunk)

    return path_to_pdf


def check_edt_info(indices: list = None, plus: int = 0):
    # permet de transfomer la date en compteur du jour dans la semaine
    # et de la semaine dans l'année (retourne l'année, le numéro de semaine et le numéro du jour)
    # utilisé pour les ids du liens pour l'edt

    current_date = date.isocalendar(datetime.now())

    num_semaine = current_date[1]
    annee = current_date[0]

    if current_date[2] > 5:
        num_semaine += 1

    while num_semaine-indices[2] < 0:
        num_semaine += 1

    url_edt = "http://applis.univ-nc.nc/gedfs/edtweb2/{}.{}/PDF_EDT_{}_{}_{}.pdf"
    url = url_edt.format(indices[0], num_semaine - indices[2] + plus, indices[1], num_semaine + plus, annee)

    edt_info = {}

    val = requests.head(url)
    val.close()

    edt_info = dict(val.headers)
    edt_info["status"] = val.status_code

    return edt_info


async def send_edt_to_chat(ctx:discord.Interaction, message:str, pdf_name: str, indices: list = None):
    path_to_pdf = f"{edt_path}/{pdf_name}"
    edt_id = indices[0]


    embed = discord.Embed(title=message, description=f"", color=discord.Color.yellow())

    #with open(path_to_pdf, 'rb') as fp:
        #await ctx.response.send_message(file=discord.File(fp, pdf_name))

    pages = convert_from_path(path_to_pdf, 150)
    i = 1
    
    for page in pages:
        file = f"{edt_path}/edt{edt_id}_{i}.jpg"
        page.save(file, 'JPEG')
        file=(discord.File(file,f"edt{edt_id}_{i}.jpg"))
        embed.set_image(url=f"attachment://edt{edt_id}_{i}.jpg")
        if i==1:
            embed.description = f"({i}/{len(pages)})" if len(pages)>1 else ""

            if type(ctx) == discord.Interaction:
                await ctx.response.send_message(embed=embed,file=file, ephemeral=True)
            else:
                await ctx.send(embed=embed, files=file)

        else:
            embed.description = f"({i}/{len(pages)})" if len(pages)>1 else ""
            await ctx.followup.send(embed=embed,file=file, ephemeral=True)
        

        i += 1



async def check_edt_update(pdf_name: str, cle_dico: str, chat_name: str, dico_licence: dict = liscInfo):
    check = compare_edt(pdf_name, dico_licence[cle_dico])
    corrupt = False

    if check == 0:
        download_edt(pdf_name, dico_licence[cle_dico])

    elif check in (2, 5, 6):
        return

    elif check in (3, 4):
        corrupt = True
        return

    servers = client.guilds
    
    for server in servers:
        chat = server.text_channels
        for channel in chat:
            if chat_name == str(channel):
                formated_role = cle_dico.upper().replace("MIAGE", " miage")
                role = discord.utils.get(server.roles, name=formated_role)
                message = ""
                if corrupt:
                    dev = discord.utils.get(server.roles, name="Bot Dev")
                    message += f"Changement d'edt pour : {role.mention} (pdf corrompu, voir sur le site, en attendant un {dev.mention})\n`Ceci est une ancienne version!`"
                else:
                    message += f"Changement d'edt pour : {role.mention}"

                await send_edt_to_chat(channel, message, pdf_name, dico_licence[cle_dico])
                break


# -------------------------------------- EDT UPDATE ------------------------------

@Lib.app.tasks(seconds=1800)
async def check_edt_lisc():
    if not launch_check_edt:
        return

    this_time = datetime.now()
    role_liste = [
        ["l4t7.pdf", "l4t7", "edt-4"], ["l2t5.pdf", "l2t5", "edt-2"], ["l1t5.pdf", "l1t5", "edt-1"],
        ["l2t7.pdf", "l2t7", "edt-2"], ["l1t7.pdf", "l1t7", "edt-1"], ["l3t5.pdf", "l3t5", "edt-3"],
        ["l3t7.pdf", "l3t7", "edt-3"], ["l3t7miage.pdf", "l3t7miage", "edt-m"], ["l4t7miage.pdf", "l4t7miage", "edt-m"]
    ]

    if not (6 <= this_time.hour <= 22):
        return

    for i in range(len(role_liste)):
        try:
            await check_edt_update(*role_liste[i])
        except Exception:
            pass
        await asyncio.sleep(30)
