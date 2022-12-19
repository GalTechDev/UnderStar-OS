from system.lib import *
from typing import Optional, Union, Any
from system.app.apt import install, uninstall
Lib = Lib_UsOS()

"""class lang_select(discord.ui.Select):
    def __init__(self) -> None:
        super().__init__(placeholder=f"{Lib.get_lang_ref(10, langage)}",max_values=1,min_values=1,options=[discord.SelectOption(label=lang,description="100%") for lang in Lib.get_lang_ref(all_lang_ref, langage)])
    
    async def callback(self, interaction: discord.Interaction):
        langage = self.values[0]
        embed = discord.Embed(title=f"{Lib.get_lang_ref(11, langage)}", description=f"{Lib.get_lang_ref(10, langage)}", color=discord.Color.blue())
        embed.add_field(name=f"{Lib.get_lang_ref(12, langage)} : {Lib.get_lang_ref(0, langage)}", value="100%")
        lang_view=langage_view()
        await interaction.response.edit_message(embed=embed,view=lang_view)
"""

async def valide_intaraction(interaction:discord.Interaction):
    try:
        await interaction.response.send_message()
    except Exception as error:
        pass
        print(error)

#----------------------- modal ----------------------------


# --------------------- select ----------------------------

class App_select(discord.ui.Select):
    def __init__(self, ctx: discord.Interaction, options) -> None:
        super().__init__(placeholder=f"Choisi une application",max_values=1,min_values=1,options=options)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        app = self.values[0]
        await app_config_menu(self.ctx, app)



#----------------------- view -----------------------------

class Back_view(discord.ui.View):
    def __init__(self, ctx, back_menu, args=[], *, timeout=180):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.back_menu = back_menu
        self.args = args


    @discord.ui.button(label="Retour",style=discord.ButtonStyle.gray)
    async def back_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await self.back_menu(self.ctx, *self.args)
        await valide_intaraction(interaction)


class Admin_view(Back_view):
    def __init__(self, ctx, back, *, timeout=180):
        super().__init__(ctx=ctx, back_menu=back, timeout=timeout)
        self.ctx = ctx


class App_view(Back_view):
    def __init__(self, ctx, back, *, timeout=180):
        super().__init__(ctx=ctx, back_menu=back, timeout=timeout)
        self.ctx = ctx
        i=0
        options=[]
        for app in list(Lib.store.get_apps().keys()):
            options.append(discord.SelectOption(label=app, description="installé" if Lib.store.is_installed(app, ctx.guild_id) else "non installé") )
            i+=1
            if i==25:
                i=0
                self.add_item(App_select(ctx, options))
                options=[]
        if options!=[]:
            self.add_item(App_select(ctx, options))


class Langue_view(Back_view):
    def __init__(self, ctx, back, *, timeout=180):
        super().__init__(ctx=ctx, back_menu=back, timeout=timeout)
        self.ctx = ctx


class Custom_view(Back_view):
    def __init__(self, ctx, back, *, timeout=180):
        super().__init__(ctx=ctx, back_menu=back, timeout=timeout)
        self.ctx = ctx


class Update_view(Back_view):
    def __init__(self, ctx, back, *, timeout=180):
        super().__init__(ctx=ctx, back_menu=back, timeout=timeout)
        self.ctx = ctx


class Config_view(discord.ui.View):
    def __init__(self, ctx, *, timeout=180):
        super().__init__(timeout=timeout)
        self.ctx = ctx
    

    @discord.ui.button(label="Administation",style=discord.ButtonStyle.gray)
    async def admin_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await admin_menu(self.ctx)
        await valide_intaraction(interaction)


    @discord.ui.button(label="Application",style=discord.ButtonStyle.gray)
    async def app_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await app_menu(self.ctx)
        await valide_intaraction(interaction)


    @discord.ui.button(label="Langage",style=discord.ButtonStyle.gray)
    async def langue_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await langue_menu(self.ctx)
        await valide_intaraction(interaction)


    @discord.ui.button(label="Personnalisation",style=discord.ButtonStyle.gray)
    async def customisation_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await customisation_menu(self.ctx)
        await valide_intaraction(interaction)    


    @discord.ui.button(label="Mise à jour",style=discord.ButtonStyle.gray)
    async def update_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await update_menu(self.ctx)
        await valide_intaraction(interaction)

class App_config_view(Back_view):
    def __init__(self, ctx, app, back_menu, args=[], *, timeout=180):
        super().__init__(ctx, back_menu, args, timeout=timeout)
        self.downloaded = Lib.store.is_downloaded(app)
        self.instaled = Lib.store.is_installed(app, ctx.guild_id)
        label=f"{'Ajouter au serveur' if not self.instaled else 'Retirer du serveur'}"
        style = discord.ButtonStyle.primary if not self.instaled else discord.ButtonStyle.danger
        self.app = app
        self.ctx=ctx
        self.add_item(self.Add_to_serv(app=app, label=label,style=style, disabled=(not self.downloaded)))
        if self.instaled:
            self.add_item(self.Update_app(label="Mettre à jour"))


    class Add_to_serv(discord.ui.Button):
        def __init__(self, *, app, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: Optional[str] = None, disabled: bool = False, custom_id: Optional[str] = None, url: Optional[str] = None, emoji: Optional[Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: Optional[int] = None): 
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.app = app
        async def callback(self, interaction: discord.Interaction) -> Any:
            await install.install(interaction, self.app)
            await valide_intaraction(interaction)


    class Update_app(discord.ui.Button):
        def __init__(self, *, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: Optional[str] = None, disabled: bool = False, custom_id: Optional[str] = None, url: Optional[str] = None, emoji: Optional[Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: Optional[int] = None): 
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)

        async def callback(self, interaction: discord.Interaction) -> Any:
            await valide_intaraction(interaction)

# -------------------------- menu --------------------------------

async def admin_menu(ctx:discord.Interaction):
    embed = discord.Embed(title="Administation", color=theme[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=Admin_view(ctx, main_menu))


async def app_menu(ctx:discord.Interaction):
    embed = discord.Embed(title="Application", color=theme[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=App_view(ctx, main_menu))


async def langue_menu(ctx:discord.Interaction):
    embed = discord.Embed(title="Langage", color=theme[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=Back_view(ctx, main_menu))


async def customisation_menu(ctx:discord.Interaction):
    embed = discord.Embed(title="Personnalisation", color=theme[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=Back_view(ctx, main_menu))


async def update_menu(ctx:discord.Interaction):
    embed = discord.Embed(title="Mise à jour", color=theme[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=Back_view(ctx, main_menu))


async def main_menu(ctx:discord.Interaction):
    embed = discord.Embed(title="Paramètre", description="", color=theme[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    embed.add_field(name="Administation", value='\u200b')
    embed.add_field(name="Application", value='\u200b')
    embed.add_field(name="Langage", value='\u200b')
    embed.add_field(name="Personnalisation", value='\u200b')
    embed.add_field(name="Mise à jour", value='\u200b')
    try:
        await ctx.edit_original_response(embed=embed, view=Config_view(ctx))
    except Exception as error:
        pass
        print(error)


async def app_config_menu(ctx:discord.Interaction, app):
    embed = discord.Embed(title=f"Application > {app}", color=theme[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    view = App_config_view(ctx,app,app_menu)
    if not view.downloaded:
        embed.add_field(name="Application non disponible", value='\u200b')
    await ctx.edit_original_response(embed=embed, view=view)


async def permission_denied(ctx:discord.Interaction, back, *args):
    embed = discord.Embed(title="Paramètre", description="Vous n'avez pas les permissions.", color=theme[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=Back_view(ctx, back, args))


@Lib.app.slash(name="config", description="config bot", force_name=True, guilds=None)
@discord.app_commands.check(Lib.is_in_staff)
async def config(ctx:discord.Interaction):
    embed = discord.Embed(title="Chargement...", description="", color=theme[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.response.send_message(embed=embed, ephemeral=True)
    await main_menu(ctx)
