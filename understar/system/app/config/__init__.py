from understar.system import lib
from os import execv, path
from sys import executable, argv
import discord 
from .apt import install, uninstall


Lib = lib.App()
Lib.app.fusion([install, uninstall])
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

#----------------------- modal ----------------------------
class Set_app_link_modal(discord.ui.Modal):
    def __init__(self, *, name: str="", link: str="", title: str = discord.utils.MISSING, timeout: lib.Optional[float] = None, custom_id: str = discord.utils.MISSING) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.old_name = name
        self.app_name = discord.ui.TextInput(label='app_name', default=name, placeholder="Saisir le nom de l'appli", min_length=1)
        self.link = discord.ui.TextInput(label='link', default=link, placeholder="Saisir l'adresse de l'appli")
        self.add_item(self.app_name)
        self.add_item(self.link)

    class Link_not_conform(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if self.old_name=="":
            out =Lib.store.add_link(self.app_name.__str__(), self.link.__str__())
        else:
            out = Lib.store.edit_link(self.old_name, self.app_name.__str__(), self.link.__str__())
        if out:
            await lib.valide_intaraction(interaction)
        else:
            raise self.Link_not_conform()


# --------------------- select ----------------------------

class App_select(discord.ui.Select):
    def __init__(self, ctx: discord.Interaction, options) -> None:
        super().__init__(placeholder=f"Choisir une application",max_values=1,min_values=1,options=options)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        app = self.values[0]
        await app_config_menu(self.ctx, app)
        await lib.valide_intaraction(interaction)



#----------------------- view -----------------------------

class Back_view(discord.ui.View):
    def __init__(self, ctx: discord.Interaction, back_menu, args=[], *, timeout=180):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.back_menu = back_menu
        self.args = args


    @discord.ui.button(label="Retour",style=discord.ButtonStyle.gray)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.back_menu(self.ctx, *self.args)
        await lib.valide_intaraction(interaction)


class Admin_view(Back_view):
    def __init__(self, ctx: discord.Interaction, back, *, timeout=180):
        super().__init__(ctx=ctx, back_menu=back, timeout=timeout)
        self.ctx = ctx


class App_view(Back_view):
    def __init__(self, ctx: discord.Interaction, back, *, timeout=180):
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
        self.add_item(self.Set_app_link(label="Ajouter un lien"))

    class Set_app_link(discord.ui.Button):
        def __init__(self, *, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await interaction.response.send_modal(Set_app_link_modal(title="Ajouter un lien"))


class Langue_view(Back_view):
    def __init__(self, ctx: discord.Interaction, back, *, timeout=180):
        super().__init__(ctx=ctx, back_menu=back, timeout=timeout)
        self.ctx = ctx


class Custom_view(Back_view):
    def __init__(self, ctx: discord.Interaction, back, *, timeout=180):
        super().__init__(ctx=ctx, back_menu=back, timeout=timeout)
        self.ctx = ctx


class Update_view(Back_view):
    def __init__(self, ctx: discord.Interaction, back, *, update: bool=False, timeout=180):
        super().__init__(ctx=ctx, back_menu=back, timeout=timeout)
        self.ctx = ctx
        self.update = update
        self.update_button = self.Update_button(ctx=self.ctx, enabled=self.update, label="Mettre à jour")
        self.add_item(self.update_button)

    class Update_button(discord.ui.Button):
        def __init__(self, *, ctx, enabled, style: discord.ButtonStyle = discord.ButtonStyle.primary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled= not enabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.ctx = ctx

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await lib.valide_intaraction(interaction)
            await self.ctx.delete_original_response()
            await Lib.change_presence(activity=discord.Game("Updating..."), status=discord.Status.dnd)
            execv(executable, ["None", "system/app/update/update.pyw"])



class Config_view(discord.ui.View):
    def __init__(self, ctx: discord.Interaction, *, timeout=180):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        if Lib.client.info.owner.id == ctx.user.id:
            self.add_item(self.Restart_button(ctx=ctx))


    @discord.ui.button(label="Administation",style=discord.ButtonStyle.gray)
    async def admin_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await admin_menu(self.ctx)
        await lib.valide_intaraction(interaction)


    @discord.ui.button(label="Application",style=discord.ButtonStyle.gray)
    async def app_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await app_menu(self.ctx)
        await lib.valide_intaraction(interaction)


    @discord.ui.button(label="Langage",style=discord.ButtonStyle.gray)
    async def langue_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await langue_menu(self.ctx)
        await lib.valide_intaraction(interaction)


    @discord.ui.button(label="Personnalisation",style=discord.ButtonStyle.gray)
    async def customisation_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await customisation_menu(self.ctx)
        await lib.valide_intaraction(interaction)


    @discord.ui.button(label="Mise à jour",style=discord.ButtonStyle.gray)
    async def update_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await update_menu(self.ctx)
        await lib.valide_intaraction(interaction)

    class Restart_button(discord.ui.Button):
        def __init__(self, *, ctx: discord.Interaction, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label="Redémarer", disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.ctx = ctx

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await lib.valide_intaraction(interaction)
            await self.ctx.delete_original_response()
            await Lib.change_presence(activity=discord.Game("Restarting..."), status=discord.Status.dnd)
            execv(executable, ["None", path.basename(argv[0]), "sync"])


class App_config_view(Back_view):
    def __init__(self, ctx: discord.Interaction, app: str, back_menu, args=[], *, timeout=180):
        super().__init__(ctx, back_menu, args, timeout=timeout)
        self.downloaded = Lib.store.is_downloaded(app)
        self.instaled = Lib.store.is_installed(app, ctx.guild_id)
        self.app = app
        self.ctx=ctx
        owner = Lib.client.info.owner

        if self.instaled:
            self.add_item(self.Rm_to_serv(app=app, label="Retirer du server", style=discord.ButtonStyle.danger, disabled=(not self.instaled)))
        else:
            self.add_item(self.Add_to_serv(app=app, label="Ajouter au server", style=discord.ButtonStyle.primary, disabled=self.instaled))

        if owner.id == ctx.user.id:
            if self.downloaded:
                self.add_item(self.Delete(app=app, label="Supprimer", style=discord.ButtonStyle.danger, disabled=(not self.downloaded)))
            else:
                self.add_item(self.Download(app=app, label="Télécharger", style=discord.ButtonStyle.primary, disabled= (self.downloaded or not Lib.store.get_link(app))))
            self.add_item(self.Set_app_link(app=app, label="Changer le lien", style=discord.ButtonStyle.gray))
            self.add_item(self.Del_app_link(app=app, label="Supprimer le lien", style=discord.ButtonStyle.danger))

        if self.downloaded and self.instaled:
            self.add_item(self.Config_app(app=app, label="Config", style=discord.ButtonStyle.primary, disabled=(Lib.store.get_installed()[self.app]==None or Lib.store.get_installed()[self.app].Lib.app.conf_com==None)))

    async def reload(self):
        await app_config_menu(self.ctx, self.app)

    class Add_to_serv(discord.ui.Button):
        def __init__(self, *, app, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.app = app
        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await install.install(interaction, self.app)
            await self.view.reload()

    class Rm_to_serv(discord.ui.Button):
        def __init__(self, *, app, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.app = app
        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await uninstall.uninstall(interaction, self.app)
            await self.view.reload()

    class Download(discord.ui.Button):
        def __init__(self, *, app, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.app = app
        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await install.download(interaction, self.app)
            await self.view.reload()

    class Delete(discord.ui.Button):
        def __init__(self, *, app, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.app = app
        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await uninstall.delete(interaction, self.app)
            await self.view.reload()

    class Update_app(discord.ui.Button):
        def __init__(self, *, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await lib.valide_intaraction(interaction)

    class Config_app(discord.ui.Button):
        def __init__(self, *, app, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.app = app

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await Lib.store.get_installed()[self.app].Lib.app.conf_com(interaction)

    class Set_app_link(discord.ui.Button):
        def __init__(self, *, app, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.app = app

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            await interaction.response.send_modal(Set_app_link_modal(title="Changer le lien", name=self.app, link=Lib.store.get_apps()[self.app]))

    class Del_app_link(discord.ui.Button):
        def __init__(self, *, app: str, style: discord.ButtonStyle = discord.ButtonStyle.secondary, label: lib.Optional[str] = None, disabled: bool = False, custom_id: lib.Optional[str] = None, url: lib.Optional[str] = None, emoji: lib.Optional[lib.Union[str, discord.Emoji, discord.PartialEmoji]] = None, row: lib.Optional[int] = None):
            super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=emoji, row=row)
            self.app_name=app

        async def callback(self, interaction: discord.Interaction) -> lib.Any:
            Lib.store.del_link(self.app_name)

# -------------------------- menu --------------------------------

async def admin_menu(ctx: discord.Interaction):
    embed = discord.Embed(title=":gear:  Administation", color=lib.THEME[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=Admin_view(ctx, main_menu))


async def app_menu(ctx: discord.Interaction):
    embed = discord.Embed(title=":gear:  Application", color=lib.THEME[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=App_view(ctx, main_menu))


async def langue_menu(ctx: discord.Interaction):
    embed = discord.Embed(title=":gear:  Langage", color=lib.THEME[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=Back_view(ctx, main_menu))


async def customisation_menu(ctx: discord.Interaction):
    embed = discord.Embed(title=":gear:  Personnalisation", color=lib.THEME[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=Back_view(ctx, main_menu))


async def update_menu(ctx: discord.Interaction):
    embed = discord.Embed(title=":gear:  Mise à jour", description="Rechercher de mise à jour...", color=lib.THEME[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=Update_view(ctx=ctx, back=main_menu, update=False))
    last = Lib.get_last_update_stats()
    update = last > float(lib.BOT_VERSION)
    embed = discord.Embed(title=":gear:  Mise à jour", description=f"{'Vous êtes à jour.' if last <= float(lib.BOT_VERSION) else 'Nouvelle version disponible'}", color=lib.THEME[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    embed.add_field(name=f"UnderStar OS v{last}", value='\u200b')
    await ctx.edit_original_response(embed=embed, view=Update_view(ctx=ctx, back=main_menu, update=update))



async def main_menu(ctx: discord.Interaction):
    embed = discord.Embed(title=":gear:  Paramètre", description="", color=lib.THEME[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
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


async def app_config_menu(ctx: discord.Interaction, app:str):
    embed = discord.Embed(title=f":gear:  Application", color=lib.THEME[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    view = App_config_view(ctx,app,app_menu)
    embed.add_field(name=app.upper(), value=f"Téléchagé : {view.downloaded}\nInstallé : {view.instaled}")
    await ctx.edit_original_response(embed=embed, view=view)


async def permission_denied(ctx: discord.Interaction, back, *args):
    embed = discord.Embed(title=":gear:  Paramètre", description="Vous n'avez pas les permissions.", color=lib.THEME[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.edit_original_response(embed=embed, view=Back_view(ctx, back, args))


@Lib.app.slash(name="config", description="config bot", direct_command=True)
@discord.app_commands.check(Lib.is_in_staff)
async def config(ctx: discord.Interaction):
    embed = discord.Embed(title="Chargement...", description="", color=lib.THEME[Lib.guilds.get_theme_guilds(guild = ctx.guild_id)]())
    await ctx.response.send_message(embed=embed, ephemeral=True)
    await main_menu(ctx)

@Lib.event.event()
async def on_ready():
    install.Lib.init_client(Lib.client)
    uninstall.Lib.init_client(Lib.client)
