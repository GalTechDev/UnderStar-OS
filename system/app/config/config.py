from system.lib import *

Lib = Lib_UsOS()
all_lang_ref = [1,2,3]

class lang_select(discord.ui.Select):
    def __init__(self) -> None:
        super().__init__(placeholder=f"{Lib.get_lang_ref(10, langage)}",max_values=1,min_values=1,options=[discord.SelectOption(label=lang,description="100%") for lang in Lib.get_lang_ref(all_lang_ref, langage)])

    async def callback(self, interaction: discord.Interaction):
        langage = self.values[0]
        embed = discord.Embed(title=f"{Lib.get_lang_ref(11, langage)}", description=f"{Lib.get_lang_ref(10, langage)}", color=discord.Color.blue())
        embed.add_field(name=f"{Lib.get_lang_ref(12, langage)} : {Lib.get_lang_ref(0, langage)}", value="100%")
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
        embed = discord.Embed(title=f"{Lib.get_lang_ref(18, langage)}", description=f"{Lib.get_lang_ref(19, langage)}", color=discord.Color.blue())
        embed.add_field(name=f"{Lib.get_lang_ref(11, langage)} 🌎", value=f"{Lib.get_lang_ref(9, langage)}")
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
        embed = discord.Embed(title=f"{Lib.get_lang_ref(11, langage)}", description=f"{Lib.get_lang_ref(10, langage)}", color=discord.Color.blue())
        embed.add_field(name=f"{Lib.get_lang_ref(12, langage)} : {Lib.get_lang_ref(0, langage)}", value="100%")
        lang_view=langage_view()
        await interaction.response.edit_message(embed=embed,view=lang_view)


class start_view(discord.ui.View):
    def __init__(self, *, timeout=180) -> None:
        super().__init__(timeout=timeout)

    @discord.ui.button(label=f"{Lib.get_lang_ref(17, langage)}",style=discord.ButtonStyle.gray)
    async def lang_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        embed = discord.Embed(title=f"{Lib.get_lang_ref(18, langage)}", description=f"{Lib.get_lang_ref(19, langage)}", color=discord.Color.blue())
        embed.add_field(name=f"{Lib.get_lang_ref(11, langage)} 🌎", value=f"{Lib.get_lang_ref(9, langage)}")
        conf_view=config_view()
        await interaction.response.send_message(embed=embed, view=conf_view, ephemeral=True)

@Lib.app.slash(name="config", description="config bot", force_name=True)
async def config(ctx:discord.Interaction):
    embed = discord.Embed(title=f"{Lib.get_lang_ref(18, langage)}", description=f"{Lib.get_lang_ref(19, langage)}", color=discord.Color.blue())
    embed.add_field(name=f"{Lib.get_lang_ref(11, langage)} 🌎", value=f"{Lib.get_lang_ref(9, langage)}")
    conf_view=config_view()
    await ctx.response.send_message(embed=embed, view=conf_view, ephemeral=True)
