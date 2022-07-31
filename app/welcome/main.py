import discord

global client
client=None
def __init__(bot_client):
    global client
    client=bot_client
    init_event()
    

classbot_folder = "app/test"
plante_verte = f"{classbot_folder}/team_plante_verte.png"
welcome_message = """
Bienvenue {}, dans le serveur

Si tu as la moindre question, n'hésite pas a demander de l'aide
"""
def init_event():
    @client.event
    async def on_member_join(ctx):
        if ctx.guild.id != 649021344058441739:
            return

        channel = ctx.guild.get_channel(649035534747959299)
        embed = discord.Embed(title="Bienvenu!", description=welcome_message.format(ctx.mention), color=discord.Color.blue())
        # embed.set_author(name='Bienvenu!')
        name = "team_plante_verte.png"
        file = discord.File(plante_verte, filename=name)
        embed.set_image(url=f"attachment://{name}")
        await channel.send(file=file, embed=embed)


    @client.event
    async def on_member_remove(ctx):
        if ctx.guild.id != 649021344058441739:
            return

        channel = ctx.guild.get_channel(649035534747959299)
        await channel.send(f"Oh non! {ctx.name} nous a quitté!")

command=[]
task=[]