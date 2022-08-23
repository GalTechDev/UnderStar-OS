from dis import disco
import discord
from discord.ext import commands
import system.lib as lib

global client
client=None

global counter
counter=0

all_lang_ref = [1,2,3]


def __init__(bot_client:commands.Bot):
    global client
    client=bot_client


class lang_select(discord.ui.Select):
    def __init__(self) -> None:
        super().__init__(placeholder=f"{lib.get_lang_ref(10, lib.langage)}",max_values=1,min_values=1,options=[discord.SelectOption(label=lang,description="100%") for lang in lib.get_lang_ref(all_lang_ref, lib.langage)])

    async def callback(self, interaction: discord.Interaction):
        lib.langage = self.values[0]
        embed = discord.Embed(title=f"{lib.get_lang_ref(11, lib.langage)}", description=f"{lib.get_lang_ref(10, lib.langage)}", color=discord.Color.blue())
        embed.add_field(name=f"{lib.get_lang_ref(12, lib.langage)} : {lib.get_lang_ref(0, lib.langage)}", value="100%")
        lang_view=langage_view()
        await interaction.response.edit_message(embed=embed,view=lang_view)


class edit_lang_view(discord.ui.View):
    def __init__(self, timeout=180) -> None:
        super().__init__(timeout=timeout)
        self.add_item(lang_select())

    
class langage_view(discord.ui.View):
    def __init__(self, *, timeout=180) -> None:
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Retour",style=discord.ButtonStyle.gray)
    async def back_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        embed = discord.Embed(title=f"{lib.get_lang_ref(18, lib.langage)}", description=f"{lib.get_lang_ref(19, lib.langage)}", color=discord.Color.blue())
        embed.add_field(name=f"{lib.get_lang_ref(11, lib.langage)} 🌎", value=f"{lib.get_lang_ref(9, lib.langage)}")
        conf_view=config_view()
        await interaction.response.edit_message(embed=embed, view=conf_view)

    @discord.ui.button(label="Modifier",style=discord.ButtonStyle.gray)
    async def edit_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        modif_view=edit_lang_view()
        await interaction.response.edit_message(view=modif_view)

class config_view(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="🌎",style=discord.ButtonStyle.gray)
    async def lang_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        embed = discord.Embed(title=f"{lib.get_lang_ref(11, lib.langage)}", description=f"{lib.get_lang_ref(10, lib.langage)}", color=discord.Color.blue())
        embed.add_field(name=f"{lib.get_lang_ref(12, lib.langage)} : {lib.get_lang_ref(0, lib.langage)}", value="100%")
        lang_view=langage_view()
        await interaction.response.edit_message(embed=embed,view=lang_view)


class start_view(discord.ui.View):
    def __init__(self, *, timeout=180) -> None:
        super().__init__(timeout=timeout)

    @discord.ui.button(label=f"{lib.get_lang_ref(17, lib.langage)}",style=discord.ButtonStyle.gray)
    async def lang_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        embed = discord.Embed(title=f"{lib.get_lang_ref(18, lib.langage)}", description=f"{lib.get_lang_ref(19, lib.langage)}", color=discord.Color.blue())
        embed.add_field(name=f"{lib.get_lang_ref(11, lib.langage)} 🌎", value=f"{lib.get_lang_ref(9, lib.langage)}")
        conf_view=config_view()
        await interaction.response.send_message(embed=embed, view=conf_view, ephemeral=True)

async def config(ctx:commands.context.Context):
    conf_view=start_view()
    await ctx.send(view=conf_view)

command=[lib.Command(command=config, name="config", aliases=["config"])]
task=[]