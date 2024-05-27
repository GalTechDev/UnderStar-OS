import json
import os

class App_store:
    """"""
    def __init__(self, installed_app) -> None:
        self.installed_app = installed_app
        self.app_store_path: str = os.path.join("save", "system", "app_store.json")
        self.guilds_path: str = os.path.join("save", "system", "guilds.json")

    def get_apps(self) -> dict:
        """Give a dict object {"app_name":"app_link",}"""

        with open(self.app_store_path, encoding="utf8") as file:
            data = json.load(file)

        return data

    def get_installed(self):
        """"""
        return self.installed_app

    def is_in_store(self, app_name: str) -> bool:
        """"""
        apps = self.get_apps()
        return app_name in list(apps.keys())

    def is_downloaded(self, app_name: str) -> bool:
        apps = self.get_installed()
        return app_name in list(apps.keys())

    def is_installed(self, app_name: str, guild_id: int) -> bool:
        with open(self.guilds_path, encoding="utf8") as file:
            data = json.load(file)

        return app_name in data[str(guild_id)]["apps"]

    def get_guilds_installed(self, app_name: str) -> list:
        with open(self.guilds_path, encoding="utf8") as file:
            data = json.load(file)

        guilds: list = []

        for guild_id in data.keys():
            if app_name in data[str(guild_id)]["apps"]:
                guilds.append(int(guild_id))

        return guilds

    def factorize_store(self):
        with open(self.app_store_path, encoding="utf8") as file:
            return json.load(file)

    def get_link(self, app_name: str) -> str:
        store = self.factorize_store()

        if not (app_name in store.keys()):
            return None

        app_link = store[app_name]
        return app_link

    def add_link(self, app_name: str, app_link: str) -> None:
        store = self.factorize_store()

        if app_name in store.keys():
            return False

        store[app_name] = app_link

        with open(self.app_store_path, "w", encoding="utf8") as file:
            file.write(json.dumps(store))

        return True

    def edit_link(self, old_name: str, app_name: str, app_link: str) -> None:
        store = self.factorize_store()

        old_link = store.pop(old_name)

        if app_name in store.keys():
            store[old_name] = old_link
            return False

        store[app_name] = app_link

        with open(self.app_store_path, "w", encoding="utf8") as file:
            file.write(json.dumps(store))

        return True

    def del_link(self, app_name: str) -> None:
        store = self.factorize_store()
        store.pop(app_name)

        with open(self.app_store_path, "w", encoding="utf8") as file:
            file.write(json.dumps(store))
