from understar.system import lib
from shutil import rmtree
import discord
import json
Lib = lib.App()

#@Lib.app.slash(name="uninstall", description="uninstall from this server", guilds=None)
#@discord.app_commands.check(Lib.is_in_staff)
async def uninstall(ctx:discord.Interaction,app_name:str):
    if Lib.store.is_installed(app_name, ctx.guild_id):
        with open("save/system/guilds.json") as file:
            guilds = json.load(file)

        guilds[str(ctx.guild_id)]["apps"].remove(app_name)

        with open("save/system/guilds.json", "w") as file:
            file.write(json.dumps(guilds))

        await ctx.response.send_message(f"Application désinstallée", ephemeral=True)
    else:
        await ctx.response.send_message(f"Application déjà désinstallée", ephemeral=True)

#@Lib.app.slash(name="delete", description="delete from machine", guilds=None)
#@discord.app_commands.check(Lib.is_in_staff)
async def delete(ctx:discord.Interaction, app_name:str, remove_save:bool=False):
    if Lib.store.is_downloaded(app_name):
        rmtree(f"app/{app_name}")
        app_name = app_name

        Lib.store.installed_app.all_app.pop(app_name)
        await ctx.response.send_message("Supprimé.", ephemeral=True)

    else:
        await ctx.response.send_message("Application non trouvée", ephemeral=True)
