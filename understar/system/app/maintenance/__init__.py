from understar.system import lib
import discord
Lib = lib.App()

@Lib.app.slash(name="clear", description="supprime des messages", direct_command=True)
async def clear(ctx:discord.Interaction, nombre:int = 1):
    await ctx.response.send_message('Netoyage en cour...', ephemeral=True)
    try:
        if Lib.is_in_staff(ctx):
            await ctx.channel.purge(limit=nombre+1)
            #clear.reset_cooldown(ctx)
        elif nombre < 5:
            await ctx.channel.purge(limit=nombre+1)
        else:
            await ctx.channel.purge(limit=6)
        await ctx.edit_original_response(content="Message(s) supprimé")
    except discord.errors.Forbidden:
        try:
            await ctx.edit_original_response(content='Le bot ne peut pas executer cette commande car il lui manque des autorisations. Merci de contacter le STAFF')
        except Exception as error:
            print(error)

