from git import Repo
from shutil import move, rmtree
from os import listdir, remove, path
download_folder = "download"

git_url = "https://github.com/GalTechDev/UnderStar-OS.git"
repo_dir = f"{download_folder}/os"
Repo.clone_from(git_url, repo_dir)
move("app", f"{download_folder}/os/")
move("token", f"{download_folder}/os/")

for p in listdir():
    if p not in ["download",".git"]:
        if path.isdir(p):
            rmtree(p)
        else:
            remove(p)

for p in listdir(download_folder):
    if p in [".git"]:
        continue
    move(p, "")
    if path.isdir(p):
        rmtree(f"{download_folder}/{p}")
    else:
        remove(f"{download_folder}/{p}")
    

exit(0)