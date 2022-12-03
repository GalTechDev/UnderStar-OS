from system.lib  import *


Lib = Lib_UsOS()

app_version = "1.1"
role_folder = f"role_database.json"






#----------- class ----------------
class RoleManager:
    def __init__(self, database_file):
        self.database_file = database_file
        self.role_database = {}
        #self.load_db()

    def load_db(self):
        """
        load the database from the json parsed
        """
        try:
            self.role_database = json.loads(Lib.save.read(self.database_file))
        except FileNotFoundError:
            Lib.save.read(self.database_file, mode="x").write(json.dumps("{}", indent=4))

    def save(self, database):
        """
        save the databse in the file
        """
        Lib.save.write(self.database_file, data=json.dumps(database, indent=4))
        

    async def bind(self, comId, chatId, messageId, emote, role):
        """
        will bind a reaction to a role
        """
        if str(comId) not in self.get_discords_id():
            self.add_discord(comId)

        if str(chatId) not in self.get_channels_id(comId):
            self.add_channel(comId, chatId)

        if str(messageId) not in self.get_messages_id(comId, chatId):
            self.add_message(comId, chatId, messageId)

        self.add_role(comId, chatId, messageId, emote, role)

    def add_discord(self, comId: str):
        """
        Add a comId to the database
        """
        self.role_database[str(comId)] = {}

    def add_channel(self, comId: str, chatId: str):
        """
        Add a channelId to the database
        """
        self.role_database[str(comId)][str(chatId)] = {}

    def add_message(self, comId, chatId, messageId):
        self.role_database[str(comId)][str(chatId)][str(messageId)] = {}

    def add_role(self, comId, chatId, messageId, emote, role):
        self.role_database[str(comId)][str(chatId)][str(messageId)][str(emote)] = str(role)

    def remove_discord(self, comId):
        del(self.role_database[str(comId)])

    def remove_channel(self, comId, chatId):
        del(self.role_database[str(comId)][str(chatId)])

    def remove_message(self, comId, chatId, messageId):
        del(self.role_database[str(comId)][str(chatId)][str(messageId)])

    def remove_role(self, comId, chatId, messageId, role):
        val = self.role_database[str(comId)][str(chatId)][str(messageId)]
        for key, value in val.items():
            if value == role:
                del(self.role_database[str(comId)][str(chatId)][str(messageId)][str(key)])
                break
        if self.role_database[str(comId)][str(chatId)][str(messageId)] == {}:
            del(self.role_database[str(comId)][str(chatId)][str(messageId)])

    def remove_emote(self, comId, chatId, messageId, emote):
        del(self.role_database[str(comId)][str(chatId)][str(messageId)][str(emote)])

    def get_discords_id(self):
        return [str(comId) for comId in self.role_database.keys()]

    def get_channels_id(self, comId):
        return [str(chat) for chat in self.role_database[str(comId)].keys()]

    def get_messages_id(self, comId, chatId):
        return [str(message) for message in self.role_database[str(comId)][str(chatId)].keys()]

    def get_emotes(self, comId, chatId, messageId):
        return [str(emote) for emote in self.role_database[str(comId)][str(chatId)][str(messageId)].keys()]

    def get_binded(self, comId, chatId, messageId):
        if str(comId) not in self.get_discords_id():
            return False

        if str(chatId) not in self.get_channels_id(comId):
            return False

        if str(messageId) not in self.get_messages_id(comId, chatId):
            return False

        return self.role_database[str(comId)][str(chatId)][str(messageId)]

    def get_all_channels_id(self, comId):
        liste = []
        for channel in self.get_channels_id(comId):
            liste.append(int(channel))

        return liste

    def get_all_messages_id(self, comId):
        liste = []
        for channel in self.get_channels_id(comId):
            for message in self.get_messages_id(comId, channel):
                liste.append(int(message))

        return liste

    def get_all_roles(self, comId):
        liste = []
        for channel in self.get_channels_id(comId):
            for message in self.get_messages_id(comId, channel):
                for role in self.get_binded(comId, channel, message).values():
                    liste.append(role)

        return liste

    def get_all_emotes(self, comId):
        liste = []
        for channel in self.get_channels_id(comId):
            for message in self.get_messages_id(comId, channel):
                for role in self.get_binded(comId, channel, message).keys():
                    liste.append(role)

        return liste

    def is_binded_from_role(self, comId, chatId, messageId, role):
        val = self.get_binded(comId, chatId, messageId)
        if not val:
            return False

        for key, value in val.items():
            if role == value:
                return key

        return False

    def is_binded_from_emote(self, comId, chatId, messageId, emote):
        val = self.get_binded(comId, chatId, messageId)
        if not val:
            return False

        for key, value in val.items():
            if emote == key:
                return value

        return False

    def search_message(self, messageId):
        for guild, channel in self.role_database.items():
            if messageId in channel.keys():
                return guild, channel

    def search_role(self, messageId, roleId):
        for guild, channel in self.role_database.items():
            for message, dico in channel.items():
                if roleId not in dico.values():
                    continue

                for emote, role in dico.items():
                    if roleId == role:
                        return emote

    def search_emote(self, messageId, emoteId):
        for guild, channel in self.role_database.items():
            for message, dico in channel.items():
                if emoteId not in dico.keys():
                    continue

                for emote, role in dico.items():
                    if emoteId == emote:
                        return role

role_db = RoleManager(role_folder)
#------------ Func -----------------
"""async def addrole(ctx:discord.Interaction, role_: discord.Role, emote): #aliases=["addmention", "addemoji", "addemote"]
    try:
        refId = ctx.message.reference.message_id
    except Exception:
        #await ctx.channel.send()
        return "Erreur! Pas de message lié!"

    try:
        role = role_.name
    except Exception:
        #await ctx.channel.send("Erreur! Role inexistant")
        return "Erreur! Role inexistant"

    emote = emote

    commu = ctx.guild.id
    chat = ctx.channel.id

    guild_info = client.get_guild(int(commu))
    channel = guild_info.get_channel(int(chat))
    role_message = await channel.fetch_message(int(refId))

    try:
        await role_message.add_reaction(emote)
    except Exception:
        #await ctx.channel.send()
        return "Erreur! Mauvaise emote!"

    await role_db.bind(commu, chat, refId, emote, role)
    role_db.save(role_db.role_database)

    channel = guild_info.get_channel(int(chat))
    role_message = await channel.fetch_message(ctx.message.id)
    return ""
    #await role_message.add_reaction("✅")
    #await ctx.channel.purge(limit=1)


async def removerole(ctx:discord.Interaction, role: discord.Role):

    try:
        refId = ctx.message.reference.message_id
    except Exception:
        await ctx.channel.send("Erreur! Pas de message lié!")
        return

    role_name = role.name
    commu = ctx.guild.id
    chat = ctx.channel.id

    #guild_info = client.get_guild(int(commu))

    try:
        role_db.remove_role(commu, chat, refId, role_name)
    except Exception:
        await ctx.channel.send("Erreur! Role inexistant")
        return
    
    role_db.save(role_db.role_database)

    #channel = guild_info.get_channel(int(chat))
    #role_message = await channel.fetch_message(ctx.message.id)
    #await role_message.add_reaction("✅")
    #await ctx.channel.purge(limit=1)


async def removeemote(ctx:discord.Interaction, emote):

    try:
        refId = ctx.message.reference.message_id
    except Exception:
        await ctx.channel.send("Erreur! Pas de message lié!")
        return

    role_name = emote
    commu = ctx.guild.id
    chat = ctx.channel.id

    guild_info = client.get_guild(int(commu))

    try:
        role_db.remove_emote(commu, chat, refId, role_name)
    except Exception:
        await ctx.channel.send("Erreur! Emote inexistant")
        return

    role_db.save(role_db.role_database)

    channel = guild_info.get_channel(int(chat))
    role_message = await channel.fetch_message(ctx.message.id)
    #await role_message.add_reaction("✅")
    #await ctx.channel.purge(limit=1)
"""
# -------------------------------- SLASH COMMANDE -------------------------------


@Lib.app.slash(name="addrole", description="liste des commande", guild=discord.Object(id=649021344058441739))
@discord.app_commands.check(Lib.is_in_staff)
async def addrole_slash(ctx: discord.Interaction, role: discord.Role, emote: str, message_id: str):
    refId = message_id
    role = role.name
    commu = ctx.guild.id
    chat = ctx.channel.id
    
    try:
        guild_info = Lib.client.get_guild(int(commu))
        channel = guild_info.get_channel(int(chat))
    except Exception as error:
        print(error)
    message = ""
    
    try:
        refId = int(message_id)
        role_message = await channel.fetch_message(int(refId))
        try:
            await role_message.add_reaction(emote)
        except Exception:
            message+="Erreur! Mauvaise emote!\n"
    except Exception:
        message+="Erreur! message_id invalide!\n"
    finally:
        if message != "":
            print(4, message)
            await ctx.response.send_message(message, ephemeral=True)
            return
    
    await role_db.bind(commu, chat, refId, emote, role)
    
    role_db.save(role_db.role_database)
    
    await ctx.response.send_message(f"{role} à bien été créé avec l'emote {emote}.", ephemeral=True)


@Lib.app.slash(name="removerole", description="retire le role", guild=discord.Object(id=649021344058441739))
async def removerole_slash(ctx: discord.Interaction, role: discord.Role, message_id:str):
    if not Lib.is_in_staff(ctx, True):
        await ctx.response.send_message("Vous n'avez pas les permissions pour utiliser cette commande.", ephemeral=True)
        return

    refId = message_id
    role_name = role.name
    commu = ctx.guild.id
    chat = ctx.channel.id
    guild_info = Lib.client.get_guild(int(commu))
    channel = guild_info.get_channel(int(chat))

    try:
        role_message = await channel.fetch_message(int(refId))
    except Exception:
        await ctx.response.send_message("Erreur! message_id invalide!", ephemeral=True)

    try:
        role_db.remove_role(commu, chat, refId, role_name)
    except Exception:
        await ctx.response.send_message("Erreur! Role inexistant", ephemeral=True)
        return

    role_db.save(role_db.role_database)
    await ctx.response.send_message(f"{role} à bien été retiré du message.", ephemeral=True)


@Lib.app.slash(name="removeemote", description="retir l'emote", guild=discord.Object(id=649021344058441739))
@discord.app_commands.check(Lib.is_in_staff)
async def removeemote_slash(ctx: discord.Interaction, emote: str, message_id: str):
    refId = message_id
    role_name = emote
    commu = ctx.guild.id
    chat = ctx.channel.id
    guild_info = Lib.client.get_guild(int(commu))
    channel = guild_info.get_channel(int(chat))

    try:
        role_message = await channel.fetch_message(int(refId))
    except Exception:
        await ctx.response.send_message("Erreur! message_id invalide!", ephemeral=True)

    try:
        await role_message.clear_reaction(emote)
        role_db.remove_emote(commu, chat, refId, role_name)
    except Exception:
        await ctx.response.send_message("Erreur! Emote inexistant", ephemeral=True)
        return

    role_db.save(role_db.role_database)
    await ctx.response.send_message(f"{emote} à bien été retiré du message.", ephemeral=True)

# ---------------------------------- EVENTS ------------------------------------

def init_event():
    role_db.load_db()
    @Lib.client.event
    async def on_ready():
        role_db.load_db()
        

    @Lib.client.event
    async def on_raw_reaction_add(ctx):
        if ctx.user_id == Lib.client.user.id:
            return

        message_id = str(ctx.message_id)
        chat_id = ctx.channel_id
        guild_id = ctx.guild_id
        # print(ctx.emoji.name)

        guild = discord.utils.find(lambda g: g.id == guild_id, Lib.client.guilds)
        user = await guild.fetch_member(ctx.user_id)

        val = role_db.is_binded_from_emote(guild_id, chat_id, message_id, ctx.emoji.name)

        if val:
            role = discord.utils.get(guild.roles, name=val)
            await user.add_roles(role)


    @Lib.client.event
    async def on_raw_reaction_remove(ctx):
        if ctx.user_id == Lib.client.user.id:
            return

        guild_id = ctx.guild_id

        # guild_id = 550450730192994306
        guild = discord.utils.find(lambda g: g.id == guild_id, Lib.client.guilds)
        user = await guild.fetch_member(ctx.user_id)

        val = role_db.is_binded_from_emote(guild_id, ctx.channel_id, ctx.message_id, ctx.emoji.name)

        if val:
            role = discord.utils.get(guild.roles, name=val)
            await user.remove_roles(role)

