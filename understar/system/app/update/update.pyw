from shutil import move, rmtree
import os
from sys import executable
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
    subprocess.check_call([executable, "-m", "pip", "install", "--upgrade", "understar"])

           
def is_pip_installed():
    """Vérifie si une bibliothèque est installée avec pip."""
    try:
        subprocess.check_output([executable, "-m", "pip", "show", "understar"])
        return True
    except subprocess.CalledProcessError:
        return False

if __name__=="__main__":
    if is_pip_installed():
        logging.warning("Pypi MAJ")
        pypi_maj()
    else:
        logging.warning("Git MAJ")
        git_maj()
        
    os.execv(executable, ["None", "exemple.py"])

