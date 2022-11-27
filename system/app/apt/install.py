from system.lib import *
import requests
import mimetypes
import uuid
from os import mkdir
from shutil import rmtree
import zipfile as zip
app=App()

@app.slash(name="install", description="install")
async def func(ctx:discord.Interaction, lien:str):
    try:
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
                zip_ref.extractall("app")
            print("here")
            rmtree(path_folder)

            await ctx.response.send_message("Installé")
        else:
            await ctx.response.send_message("Type d'archive non pris en charge")
    except Exception as error:
        await ctx.response.send_message(f"Une erreur c'est produit : {error}")
        print(error)