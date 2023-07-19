import json

class App_store:
    """"""
    def __init__(self, installed_app) -> None:
        self.installed_app = installed_app

    def get_apps(self) -> dict:
        """Give a dict object {"app_name":"app_link",}"""
        with open("save/system/app_store.json") as file:
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
        with open("save/system/guilds.json") as file:
            data = json.load(file)
        return app_name in data[str(guild_id)]["apps"]
    
    def get_guilds_installed(self, app_name: str) -> list:
        with open("save/system/guilds.json") as file:
            data = json.load(file)
            
        guilds = []
        for guild_id in data.keys():
            if app_name in data[str(guild_id)]["apps"]:
                guilds.append(int(guild_id))
        return guilds
    
    def get_link(self, app_name: str) -> str:
        file_path="save/system/app_store.json"
        with open(file_path) as file:
            store = json.load(file)

        if not (app_name in store.keys()):
            return None
        else: 
            app_link = store[app_name]
            return app_link

    def add_link(self, app_name: str, app_link: str) -> None:
        file_path="save/system/app_store.json"
        with open(file_path) as file:
            store = json.load(file)

        if app_name in store.keys():
            return False
        store[app_name]=app_link

        with open(file_path, "w") as file:
            file.write(json.dumps(store))
        return True

    def edit_link(self, old_name: str, app_name: str, app_link: str) -> None:
        file_path="save/system/app_store.json"
        with open(file_path) as file:
            store = json.load(file)

        old_link = store.pop(old_name)
        if app_name in store.keys():
            store[old_name]=old_link
            return False

        store[app_name]=app_link

        with open(file_path, "w") as file:
            file.write(json.dumps(store))
        return True

    def del_link(self, app_name: str) -> None:
        file_path="save/system/app_store.json"
        with open(file_path) as file:
            store = json.load(file)

        store.pop(app_name)

        with open(file_path, "w") as file:
            file.write(json.dumps(store))