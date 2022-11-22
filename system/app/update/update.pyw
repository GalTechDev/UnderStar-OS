from git import Repo
from shutil import move, rmtree
from os import listdir, remove, path, curdir
download_folder = "download/os"

git_url = "https://github.com/GalTechDev/UnderStar-OS.git"
repo_dir = f"{download_folder}"
Repo.clone_from(git_url, repo_dir)
move("app", f"{download_folder}")
move("token", f"{download_folder}")

for p in listdir():
    if p not in ["download",".git"]:
        if path.isdir(p):
            rmtree(p)
        else:
            remove(p)

for p in listdir(download_folder):
    print(listdir(download_folder))
    if p in [".git", ".gitignore"]:
        if path.isdir(f"{download_folder}/{p}"):
            rmtree(f"{download_folder}/{p}")
        else:
            remove(f"{download_folder}/{p}")
    else:
        move(f"{download_folder}/{p}", curdir)
    
exit(0)