import git
from sys import argv

git_url = "https://github.com/GalTechDev/classbot-UsOS.git"
repo_dir = "system/download/classbot"
git.Repo.clone_from(git_url, repo_dir)

exit(0)