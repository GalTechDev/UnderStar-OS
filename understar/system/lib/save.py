import json
from os import remove, listdir, mkdir, path
from shutil import rmtree

class Save:
    """"""
    def __init__(self, app_name: str) -> None:
        self.path = None
        self.app_name = app_name
        self.save_path = "save/app"

    def add_file(self, name: str, path: str="", over_write: bool=False) -> None:
        """ajoute un fichier à sauvegarder"""
        try:
            if path=="":
                full_path=f"{self.save_path}/{self.app_name}/{name}"
            else:
                full_path=f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"

            with open(full_path, "x"):
                pass

        except (FileExistsError):
            if over_write:
                if path=="":
                    full_path=f"{self.save_path}/{self.app_name}/{name}"
                else:
                    full_path=f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"
                remove(full_path)
                self.add_file(name,path,over_write)
            else:
                raise FileExistsError

    def open(self, name: str, path: str=""):
        if path=="":
            path = f"{self.save_path}/{self.app_name}/{name}"
        else:
            path = f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"

        with open(path) as file:
            return file

    def read(self, name, path="", binary_mode=False):
        if path=="":
            path = f"{self.save_path}/{self.app_name}/{name}"
        else:
            path = f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"

        with open(path, 'rb' if binary_mode else 'r') as file:
            return file.read()

    def write(self, name, path="", data="", binary_mode=False):
        if path=="":
            path = f"{self.save_path}/{self.app_name}/{name}"
        else:
            path = f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"

        with open(path, 'wb' if binary_mode else 'w') as file:
            file.write(data)

    def json_read(self, name, path=""):
        if path=="":
            path = f"{self.save_path}/{self.app_name}/{name}"
        else:
            path = f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"

        with open(path, 'r') as file:
            return json.load(file)

    def get_files(self, path=""):
        return listdir(f"{self.save_path}/{self.app_name}/{path}")

    def existe(self, name, path=""):
        return name in self.get_files(path)

    def remove_file(self, name, path=""):
        if path=="":
            path = f"{self.save_path}/{self.app_name}/{name}"
        else:
            path = f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}"

        remove(f"{path}/{self.app_name}/{name}")


    def add_folder(self, path="", ignor_exception=True):
        try:
            mkdir(f"{self.save_path}/{self.app_name}/{path}")
        except:
            if not ignor_exception:
                raise Exception(f"Path: {path} can't be create")

    def remove_folder(self, path=""):
        rmtree(f"{self.save_path}/{self.app_name}/{path}")
        pass

    def get_tree(self, path=""):
        tree={}
        for folder in listdir(f"{self.save_path}/{self.app_name}/{path}"):
            if path.isdir(f"{self.save_path}/{self.app_name}/{path}/{folder}"):
                tree[folder]=self.get_tree(f"{path}/{folder}")
        return tree

    def get_full_path(self, name, path=""):
        if path=="":
            path=(f"{self.save_path}/{self.app_name}/{name}")
        else:
            path=(f"{self.save_path}/{self.app_name}/{path+'/' if path[-1]!='/' else ''}{name}")
        return path