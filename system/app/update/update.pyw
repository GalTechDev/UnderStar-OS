import requests
import uuid
from shutil import move, rmtree
from os import mkdir, listdir, remove, path, curdir, system
import zipfile as zip

download_folder = "download/os"

git_url = "https://github.com/GalTechDev/UnderStar-OS/archive/refs/heads/main.zip"

response = requests.get(git_url)
folder = uuid.uuid4()
content_type = response.headers['content-type']
extension = mimetypes.guess_extension(content_type)
path_folder = f"download/{folder}"
mkdir(path_folder)
file_path = f"{path_folder}/file{extension}"
open(file_path, "wb").write(response.content)
if zip.is_zipfile(file_path):
    with zip.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(path_folder)

if len(listdir(path_folder))==2:
    remove(file_path)
    old_name = listdir(path_folder)[0]
    move(f"{path_folder}/{old_name}/{old_name}", f"{path_folder}/{old_name}")
else:
    exit()

#repo_dir = f"{download_folder}"
#Repo.clone_from(git_url, repo_dir)
move("app", f"{path_folder}/{old_name}")
move("token", f"{path_folder}/{old_name}")
move("save", f"{path_folder}/{old_name}")

for p in listdir():
    if p not in ["download",".git"]:
        if path.isdir(p):
            rmtree(p)
        else:
            remove(p)

for p in listdir(f"{path_folder}/{old_name}"):
    #print(listdir(download_folder))
    if p in [".git"]:
        pass
    else:
        move(f"{path_folder}/{old_name}/{p}", curdir)
    
system('rmdir /S /Q "{}"'.format(path_folder))
system('start understar.py')
