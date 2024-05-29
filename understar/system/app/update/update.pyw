import requests
import uuid
from shutil import move, rmtree
import os
from sys import argv, executable
import mimetypes
import zipfile as zip

download_folder = os.path.join("download", "os")

git_url = "https://github.com/GalTechDev/UnderStar-OS/archive/refs/heads/main.zip"

response = requests.get(git_url)
folder = uuid.uuid4()
content_type = response.headers['content-type']
extension = mimetypes.guess_extension(content_type)
path_folder = os.path.join("download", f"{folder}")
os.mkdir(path_folder)
file_path = os.path.join(f"{path_folder}", f"file{extension}")
open(file_path, "wb").write(response.content)

if zip.is_zipfile(file_path):
    with zip.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(path_folder)

if len(os.listdir(path_folder))==2:
    os.remove(file_path)
    old_name = os.listdir(path_folder)[0]
    rmtree(os.path.join(f"{path_folder}", f"{old_name}", "save"))

else:
    exit()

#repo_dir = f"{download_folder}"
#Repo.clone_from(git_url, repo_dir)
move("app", os.path.join(f"{path_folder}", f"{old_name}"))
move("token", os.path.join(f"{path_folder}", f"{old_name}"))
move("save", os.path.join(f"{path_folder}", f"{old_name}"))

for p in os.listdir():
    if p not in ["download",".git"]:
        if os.path.isdir(p):
            rmtree(p)

        else:
            os.remove(p)

for p in os.listdir(os.path.join(f"{path_folder}", f"{old_name}")):
    if p in [".git"]:
        pass
        
    else:
        move(os.path.join(f"{path_folder}", f"{old_name}", f"{p}"), os.curdir)

os.system('rmdir /S /Q "{}"'.format(path_folder))
os.execv(executable, ["None", "understar.py"])
