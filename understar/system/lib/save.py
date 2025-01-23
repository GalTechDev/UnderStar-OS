import json
import os
from shutil import rmtree


class Save:
    """"""
    def __init__(self, app_name: str) -> None:
        self.path = None
        self.app_name = app_name
        self.save_path = os.path.join("save", "app")

    def add_file(self, name: str, save_path: str = "", over_write: bool = False) -> None:
        """ajoute un fichier à sauvegarder"""
        try:
            full_path = self.get_full_path(name, save_path)

            with open(full_path, "x"):
                pass

        except (FileExistsError):
            if not over_write:
                raise FileExistsError

            self.remove_file(name, save_path)
            self.add_file(name, save_path, False)

    def open(self, name: str, save_path: str = "", mode="r"):
        """This function return a open file, dont forget to close it

        Args:
            name (str): _description_
            save_path (str, optional): _description_. Defaults to "".
            mode (str, optional): _description_. Defaults to "r".

        Returns:
            FileIO: a stream
        """
        save_path = self.get_full_path(name, save_path)
        file = open(save_path, mode)
        return file

    def read(self, name: str, save_path: str = "", binary_mode: bool = False):
        return self.factorize_save(name=name, save_path=save_path, mode="rb" if binary_mode else "b")

    def write(self, name, save_path: str = "", data: str = "", binary_mode: bool = False):
        return self.factorize_save(name=name, save_path=save_path, mode="wb" if binary_mode else "w", data=data)

    def json_read(self, name, save_path: str = "") -> dict:
        return json.loads(self.factorize_save(name=name, save_path=save_path, mode="r"))

    def get_files(self, save_path: str = ""):
        return os.listdir(self.get_full_path(save_path=save_path))

    def existe(self, name, save_path: str = ""):
        return name in self.get_files(save_path)

    def remove_file(self, name: str, save_path: str = ""):
        save_path = self.get_full_path(name, save_path)
        os.remove(save_path)

    def add_folder(self, save_path: str = "", ignore_exception: bool = True):
        try:
            os.mkdir(self.get_full_path(save_path=save_path))

        except Exception:
            if not ignore_exception:
                raise Exception(f"Path: {save_path} can't be create for {self.app_name}")

    def remove_folder(self, save_path: str = ""):
        rmtree(self.get_full_path(save_path=save_path))

    def get_tree(self, save_path: str = ""):
        tree: dict = {}

        for folder in os.listdir(self.get_full_path(save_path=save_path)):
            if save_path.isdir(self.get_full_path(save_path=os.path.join(save_path, folder))):
                tree[folder] = self.get_tree(os.path.join(save_path, folder))

        return tree

    def factorize_save(self, name: str, save_path: str = "", mode: str = "r", data: any = ""):
        
        save_path = self.get_full_path(name, save_path)

        encoding = "utf8" if "b" not in mode else None

        if "w" in mode:
            with open(save_path, mode, encoding=encoding) as file:
                file.write(data)

        elif "r" in mode:
            with open(save_path, mode, encoding=encoding) as file:
                return file.read()

    def get_full_path(self, name: str = "", save_path: str = ""):
        app_save_path = os.path.join(f"{self.save_path}", f"{self.app_name}")
        full_path = os.path.join(app_save_path, save_path, name)
        
        return full_path
