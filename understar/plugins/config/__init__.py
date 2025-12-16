
import discord
import os
import shutil
import git
from typing import Optional, List
from core.plugin import Plugin, slash_command
from core.permissions import Role, check_permission
from core.utils import get_logger

class ConfigView(discord.ui.View):
    def __init__(self, plugin):
        super().__init__(timeout=180)
        self.plugin = plugin

    @discord.ui.button(label="Gérer les Apps", style=discord.ButtonStyle.primary)
    async def manage_apps(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ManageAppsView(self.plugin, interaction.guild_id)
        await interaction.response.edit_message(content="**Gestion des Applications**", view=view)

    @discord.ui.button(label="Configuration du Serveur", style=discord.ButtonStyle.secondary)
    async def server_config(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ServerConfigView(self.plugin, interaction.guild_id)
        await interaction.response.edit_message(content="**Configuration du Serveur**", view=view)

class ServerConfigView(discord.ui.View):
    def __init__(self, plugin, guild_id):
        super().__init__(timeout=180)
        self.plugin = plugin
        self.guild_id = guild_id
        
    @discord.ui.select(placeholder="Choisir le rôle Manager", cls=discord.ui.RoleSelect, min_values=1, max_values=1)
    async def select_role(self, interaction: discord.Interaction, select: discord.ui.RoleSelect):
        role = select.values[0]
        # Save role
        config = self.plugin.data.get(scope="guild", id=self.guild_id, default={})
        config["manager_role_id"] = role.id
        self.plugin.data.save(config, scope="guild", id=self.guild_id)
        
        await interaction.response.send_message(f"Rôle Manager défini sur : {role.mention}", ephemeral=True)

    @discord.ui.button(label="Retour", style=discord.ButtonStyle.danger, row=1)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="**Menu Configuration**", view=ConfigView(self.plugin))

class ManageAppsView(discord.ui.View):
    def __init__(self, plugin, guild_id):
        super().__init__(timeout=180)
        self.plugin = plugin
        self.guild_id = guild_id
        self._add_app_select()

    def _add_app_select(self):
        # List all available plugins
        plugins = self.plugin.bot.kernel.plugin_manager.plugins.keys()
        options = []
        for p in plugins:
            if p == "config": continue # Skip config itself
            options.append(discord.SelectOption(label=p, value=p, description=f"Gérer l'application {p}"))
        
        if not options:
            options.append(discord.SelectOption(label="Aucune app disponible", value="none", default=True))

        select = discord.ui.Select(placeholder="Choisir une application", options=options, row=0)
        select.callback = self.select_callback
        self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        app_name = interaction.data["values"][0]
        if app_name == "none": return
        
        # Open App Details View
        view = AppDetailsView(self.plugin, app_name, self.guild_id)
        await interaction.response.edit_message(content=f"**Configuration : {app_name}**", view=view)

    @discord.ui.button(label="Retour", style=discord.ButtonStyle.danger, row=1)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="**Menu Configuration**", view=ConfigView(self.plugin))

    def __init__(self, plugin, app_name, guild_id):
        super().__init__(timeout=180)
        self.plugin = plugin
        self.app_name = app_name
        self.guild_id = guild_id
        self._update_button()

    def _update_button(self):
        # Load state
        config = self.plugin.data.get(scope="guild", id=self.guild_id, default={})
        disabled_apps = config.get("disabled_apps", [])
        is_enabled = self.app_name not in disabled_apps
        
        button = [x for x in self.children if x.label and "Activer" in x.label][0]
        button.label = "Désactiver" if is_enabled else "Activer"
        button.style = discord.ButtonStyle.danger if is_enabled else discord.ButtonStyle.success

    @discord.ui.button(label="Activer/Désactiver", style=discord.ButtonStyle.success)
    async def toggle_app(self, interaction: discord.Interaction, button: discord.ui.Button):
        config = self.plugin.data.get(scope="guild", id=self.guild_id, default={})
        disabled_apps = config.get("disabled_apps", [])
        
        if self.app_name in disabled_apps:
            disabled_apps.remove(self.app_name)
            msg = f"Application {self.app_name} **activée** pour ce serveur."
        else:
            disabled_apps.append(self.app_name)
            msg = f"Application {self.app_name} **désactivée** pour ce serveur."
        
        config["disabled_apps"] = disabled_apps
        self.plugin.data.save(config, scope="guild", id=self.guild_id)
        
        self._update_button()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(msg, ephemeral=True)

    @discord.ui.button(label="Retour", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ManageAppsView(self.plugin, self.guild_id)
        await interaction.response.edit_message(content="**Gestion des Applications**", view=view)


class ConfigPlugin(Plugin):
    def on_load(self):
        self.logger.info("Config Plugin Loaded")

    @slash_command(name="config", description="Configurer le bot", dm_permission=False)
    @check_permission(Role.GUILD_MANAGER)
    async def config(self, interaction: discord.Interaction):
        view = ConfigView(self)
        await interaction.response.send_message("**Menu Configuration**", view=view, ephemeral=True)

    @slash_command(name="install", description="Installer une app via GitHub", dm_permission=False)
    @check_permission(Role.BOT_ADMIN)
    async def install_app(self, interaction: discord.Interaction, github_url: str, token: Optional[str] = None):
        await interaction.response.defer(ephemeral=True)
        
        try:
            repo_name = github_url.split("/")[-1].replace(".git", "")
            target_dir = os.path.join("understar", "plugins", repo_name)
            
            if os.path.exists(target_dir):
                await interaction.followup.send(f"App {repo_name} déjà installée.")
                return

            if token:
                auth_url = github_url.replace("https://", f"https://{token}@")
                git.Repo.clone_from(auth_url, target_dir)
            else:
                git.Repo.clone_from(github_url, target_dir)
            
            success = await self.bot.kernel.plugin_manager.load_plugin(repo_name)
            
            if success:
                await interaction.followup.send(f"✅ {repo_name} installée et chargée !")
            else:
                await interaction.followup.send(f"⚠️ {repo_name} installée mais échec du chargement.")

        except Exception as e:
            self.logger.error(f"Installation failed: {e}")
            await interaction.followup.send(f"Erreur d'installation : {e}")

    @slash_command(name="dev_load_all", description="[DEV] Recharger tous les plugins", dm_permission=True)
    @check_permission(Role.BOT_ADMIN)
    async def dev_load_all(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await self.bot.kernel.plugin_manager.load_all_plugins()
        await interaction.followup.send("Plugins rechargés.")
