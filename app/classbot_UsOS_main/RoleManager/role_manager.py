# coding: utf-8
import json


class RoleManager:
    def __init__(self, database_file):
        self.database_file = database_file
        self.role_database = {}
        self.load_db()

    def load_db(self):
        """
        load the database from the json parsed
        """
        try:
            with open(self.database_file, "rb") as f:
                self.role_database = json.loads(f.read())
        except FileNotFoundError:
            with open(self.database_file, "w") as f:
                f.write("{}")

    def save(self, database):
        """
        save the databse in the file
        """
        with open(self.database_file, "w") as f:
            f.write(json.dumps(database, indent=4))

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
