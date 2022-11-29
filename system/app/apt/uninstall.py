from system.lib import *
from shutil import rmtree
from sys import executable, argv
from os import execv, path
Lib = Lib_UsOS()

@Lib.app.slash(name="uninstall", description="uninstall")
async def func(ctx:discord.Interaction, ref:str):
    if Lib.store.is_installed(ref):
        rmtree(f"app/{ref}")
        app_name = ref
        #app_name=app_name.replace("-", "_")
        with open("save/system/installed_app.py") as file:
            content = file.readlines()

        found = False
        for i,line in enumerate(content):
            if app_name in line:
                found = True
                break

        content.pop(i)
        content[-1] = content[-1].replace(f'"{app_name}":{app_name},', "")
                
        with open("save/system/installed_app.py", "w") as file:
            file.writelines(content)
        await ctx.response.send_message("Supprimé\nRedémarage...", ephemeral=True)
        await Lib.change_presence(discord.Game("Restarting..."), discord.Status.dnd)
        execv(executable, ["None", path.basename(argv[0]), "sync"])
        
    else:
        await ctx.response.send_message("Application non trouvé", ephemeral=True)
    