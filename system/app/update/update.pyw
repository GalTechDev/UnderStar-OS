from git import Repo
from sys import argv

git_url = "https://github.com/GalTechDev/UnderStar-OS"
repo_dir = "system/download"
Repo.clone_from(git_url, repo_dir)

exit(0)