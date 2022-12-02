from system.lib import *
import requests
import mimetypes
import uuid
from os import mkdir, listdir,remove, rename, execv, path,removedirs
from sys import executable, argv
from shutil import rmtree, move
import zipfile as zip

Lib = Lib_UsOS()

@Lib.app.slash(name="install", description="install")
async def install(ctx:discord.Interaction, ref:str):
    if Lib.store.is_installed(ref):
        await ctx.response.send_message("Application déjà installé")
        return

    try:
        if Lib.store.is_in_store(ref):
            lien = Lib.store.get_apps()[ref]
        else:
            lien = ref
        response = requests.get(lien)
        folder = uuid.uuid4()
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        path_folder = f"download/{folder}"
        mkdir(path_folder)
        file_path = f"{path_folder}/file{extension}"
        open(file_path, "wb").write(response.content)
        if zip.is_zipfile(file_path):
            with zip.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(path_folder)

            if len(listdir(path_folder))==2:
                remove(file_path)
                app_name = listdir(path_folder)[0]
                move(f"{path_folder}/{app_name}", "app")
                rename(f"app/{app_name}", f'app/{app_name.replace("-", "_")}')
                app_name=app_name.replace("-", "_")
                mkdir(f"save/app/{app_name}")
                with open("save/system/installed_app.py") as file:
                    content = file.readlines()
                content.insert(0, f"import app.{app_name}.main as {app_name}\n")
                content[-1]=content[-1][:-1]+f'"{app_name}":{app_name}'+",}"
                
                with open("save/system/installed_app.py", "w") as file:
                    file.writelines(content)

                rmtree(path_folder)

                await ctx.response.send_message("Installé\nRedémarage...", ephemeral=True)
                await Lib.change_presence(activity=discord.Game("Restarting..."), status=discord.Status.dnd)
                execv(executable, ["None", path.basename(argv[0]), "sync"])

            else:
                await ctx.response.send_message("Plus d'un élément trouvé dans l'archive, installation ignoré")
                rmtree(path_folder)

        else:
            await ctx.response.send_message("Type d'archive non pris en charge")
    except Exception as error:
        await ctx.response.send_message(f"Une erreur c'est produit : {error}")
        print(error)

#classbot_UsOS_main