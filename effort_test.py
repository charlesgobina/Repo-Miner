"""File to test developers effort"""

from configparser import ConfigParser
from developers_effort import DevEffort

config = ConfigParser()
config.read('config.ini')

developers_effort = DevEffort("commits_hash_test.json", config)
developers_effort.mine_projects()
# developers_effort.organize_by_refactoring()
