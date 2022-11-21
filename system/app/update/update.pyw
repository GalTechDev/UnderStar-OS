from git import Repo

from shutil import move, rmtree
from os import listdir
download_folder = "download"

git_url = "https://github.com/GalTechDev/UnderStar-OS.git"
repo_dir = f"{download_folder}/os"
Repo.clone_from(git_url, repo_dir)
move("app", f"{download_folder}/os/")
move("token", f"{download_folder}/os/")

for path in listdir():
    if path not in ["download",".git"]:
        rmtree(path)

for path in listdir(download_folder):
    if path == ".git":
        continue
    move(path, "")
    rmtree(f"{download_folder}/{path}")

exit(0)