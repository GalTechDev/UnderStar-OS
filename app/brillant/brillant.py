import discord
from discord.ext import commands
import system.lib as lib

global client
client=None
def __init__(bot_client):
    global client
    client=bot_client
    

async def bonjour(ctx:commands.context.Context, nom):
    await ctx.reply("Coucou " + nom)
    if nom == "Shiro":
        embed = discord.Embed(title="Wouhou")
        embed.add_field(name="Shirooo", value="tu es fou")
        embed.set_image(url="https://medias.spotern.com/spots/w640/67/67181-1532336916.jpg") 
        await ctx.send(embed=embed)



command=[lib.Command(name="bonjour",command=bonjour,aliases=["salut"])]
task=[]