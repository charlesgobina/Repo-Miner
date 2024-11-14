"""File to test developers effort"""

import os
from configparser import ConfigParser
from developers_effort import DevEffort

config = ConfigParser()
config.read('config.ini')

developers_effort = DevEffort("commits_hash_test", config)

for json_file in os.listdir(developers_effort.json_path):
    developers_effort.mine_projects(json_file)
# developers_effort.organize_by_refactoring()
