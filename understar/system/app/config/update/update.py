from shutil import move, rmtree
import os
from sys import argv
import git
import subprocess
import logging

def git_maj():
    """Met à jour une bibliothèque installée via git."""
    download_folder = os.path.join("download", "os")

    git_url = "https://github.com/GalTechDev/UnderStar-OS/"

    git.Repo.clone_from(git_url, download_folder)

    rmtree("understar")
    move(os.path.join(download_folder, "understar"), "understar")

    rmtree(download_folder)

def pypi_maj():
    """Met à jour une bibliothèque installée via pip."""
    subprocess.check_call(["pip", "install", "--upgrade", "understar"])

if __name__=="__main__":
    if "pypi" in argv:
        logging.warning("Pypi MAJ")
        pypi_maj()
    elif "git" in argv:
        logging.warning("Git MAJ")
        git_maj()
    else:
        exit(0)
