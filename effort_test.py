"""File to test developers effort"""

import os
from configparser import ConfigParser
from git import Repo
from developers_effort import DevEffort

config = ConfigParser()
config.read('config.ini')

developers_effort = DevEffort("commits_hash", config)
GITHUB_URL = "https://github.com/apache"
OUTPUT_DIR = f"{config['output']['path']}"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for json_file in os.listdir(developers_effort.json_path):
    project_name = json_file[:-5]
    remote_repo = f"{GITHUB_URL}/{project_name}.git"
    local_repo = f"{config['cloned_repos']['repos_path']}/{project_name}"

    if os.path.isdir(local_repo):
        print(f"Project {local_repo} already cloned.")
    else:
        Repo.clone_from(remote_repo, local_repo)

    developers_effort.mine_projects(json_file)
