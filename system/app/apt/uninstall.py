from system.lib import *
from shutil import rmtree

Lib = Lib_UsOS()

@Lib.app.slash(name="uninstall", description="uninstall")
async def func(ctx:discord.Interaction, ref:str):
    if App_store.is_installed(ref):
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
        
        await ctx.response.send_message("Supprimé", ephemeral=True)
    else:
        await ctx.response.send_message("Application non trouvé", ephemeral=True)
    