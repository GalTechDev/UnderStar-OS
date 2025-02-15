from understar.system import lib
import requests
import mimetypes
import uuid
import os
from shutil import rmtree, move
import zipfile as zip
import discord
import json
import logging

Lib = lib.App()

#@Lib.app.slash(name="download", description="download", guilds=None)
#@discord.app_commands.check(Lib.is_in_staff)
async def download(ctx:discord.Interaction, app_name: str, link: str = ""):
    if Lib.store.is_downloaded(app_name):
        await ctx.response.send_message("Application déjà téléchargée", ephemeral=True)
        return

    try:
        if Lib.store.is_in_store(app_name):
            lien = Lib.store.get_apps()[app_name]

        else:
            Lib.store.add_link(app_name=app_name, app_link=link)
            lien = link

        response = requests.get(lien)
        folder = uuid.uuid4()
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        path_folder = os.path.join(f"download", f"{folder}")
        os.mkdir(path_folder)
        file_path = os.path.join(f"{path_folder}", f"file{extension}")

        with open(file_path, "wb") as f:
            f.write(response.content)

        if zip.is_zipfile(file_path):
            with zip.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(path_folder)

            if len(os.listdir(path_folder))==2:
                os.remove(file_path)
                old_name = os.listdir(path_folder)[0]
                move(os.path.join(f"{path_folder}", f"{old_name}"), "app")
                os.rename(os.path.join(f"app", f"{old_name}"), os.path.join(f"app", app_name.replace("-", "_")))

                rmtree(path_folder)

                Lib.store.installed_app.update({app_name:None})
                await ctx.response.send_message("Installé", ephemeral=True)

            else:
                await ctx.response.send_message("Plus d'un élément trouvé dans l'archive, installation ignorée", ephemeral=True)
                rmtree(path_folder)

        else:
            await ctx.response.send_message("Type d'archive non prise en charge", ephemeral=True)

    except Exception as error:
        await ctx.response.send_message(f"Une erreur s'est produite : {error}", ephemeral=True)
        logging.error(error)


#@Lib.app.slash(name="install", description="install", guilds=None)
#@discord.app_commands.check(Lib.is_in_staff)
async def install(ctx:discord.Interaction,app_name:str):
    if Lib.store.is_downloaded(app_name):
        with open(os.path.join("save", "system", "guilds.json")) as file:
            guilds = json.load(file)

        guilds[str(ctx.guild_id)]["apps"].append(app_name)

        with open(os.path.join("save", "system", "guilds.json"), "w") as file:
            file.write(json.dumps(guilds))

        await ctx.response.send_message("Application installé", ephemeral=True)

    else:
        if Lib.store.is_installed(app_name, ctx.guild_id):
            await ctx.response.send_message("Application déjà installé", ephemeral=True)

        else:
            await ctx.response.send_message("Cette application n'est pas disponible", ephemeral=True)

#@Lib.app.slash(name="add_product", description="add a app reference in store", guilds=None)
#@discord.app_commands.check(Lib.is_in_staff)
async def add_link(ctx:discord.Interaction,app_name:str, link:str):
    Lib.store.add_link(app_name, link)
    await ctx.response.send_message("Application ajouté au store", ephemeral=True)
