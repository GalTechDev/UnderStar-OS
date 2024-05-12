import json
from os import remove, listdir, mkdir
from shutil import rmtree


class Save:
    """"""
    def __init__(self, app_name: str) -> None:
        self.path = None
        self.app_name = app_name
        self.save_path = "save/app"
        self.app_path = f"{self.save_path}/{self.app_name}"

    def add_file(self, name: str, save_path: str = "", over_write: bool = False) -> None:
        """ajoute un fichier à sauvegarder"""
        try:
            full_path = self.get_full_path(name, save_path)

            with open(full_path, "x"):
                pass

        except (FileExistsError):
            if not over_write:
                raise FileExistsError

            full_path = self.get_full_path(name, save_path)
            remove(full_path)
            self.add_file(name, save_path, over_write)

    def open(self, name: str, save_path: str = ""):
        return self.factorize_save(name=name, save_path=save_path, mode="r")

    def read(self, name: str, save_path: str = "", binary_mode: bool = False):
        return self.factorize_save(name=name, save_path=save_path, mode="r").read()

    def write(self, name, save_path: str = "", data: str = "", binary_mode: bool = False):
        return self.factorize_save(name=name, save_path=save_path, mode='wb' if binary_mode else 'w', data=data)

    def json_read(self, name, save_path: str = ""):
        return json.load(self.factorize_save(name=name, save_path=save_path, mode="r"))

    def get_files(self, save_path: str = ""):
        return listdir(f"{self.app_path}/{save_path}")

    def existe(self, name, save_path: str = ""):
        return name in self.get_files(save_path)

    def remove_file(self, name: str, save_path: str = ""):
        save_path = self.get_full_path(name, save_path)
        remove(f"{save_path}/{self.app_name}/{name}")

    def add_folder(self, save_path: str = "", ignore_exception: bool = True):
        try:
            mkdir(f"{self.app_path}/{save_path}")

        except:
            if not ignore_exception:
                raise Exception(f"Path: {save_path} can't be create")

    def remove_folder(self, save_path: str = ""):
        rmtree(f"{self.app_path}/{save_path}")
        pass

    def get_tree(self, save_path: str = ""):
        tree: dict = {}

        for folder in listdir(f"{self.app_path}/{save_path}"):
            if save_path.isdir(f"{self.app_path}/{save_path}/{folder}"):
                tree[folder] = self.get_tree(f"{save_path}/{folder}")

        return tree

    def factorize_save(self, name: str, save_path: str = "", mode: str = "r", data: any = ""):
        if not save_path:
            save_path = f"{self.app_path}/{name}"

        else:
            save_path = f"{self.app_path}/{save_path+'/' if save_path[-1]!='/' else ''}{name}"

        encoding = "utf8" if "b" not in mode else None

        if "w" in mode:
            with open(save_path, mode, encoding=encoding) as file:
                file.write(data)

        elif "r" in mode:
            with open(save_path, mode, encoding=encoding) as file:
                return file

    def get_full_path(self, name: str , save_path: str = ""):
        if not save_path:
            save_path = f"{self.app_path}/{save_path}"
        else:
            save_path = f"{self.app_path}/{save_path+'/' if save_path[-1]!='/' else ''}{name}"

        return save_path
