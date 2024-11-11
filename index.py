'''
TBW'''
import os
import sys
from get_github_url import CSVHandler
from refactoring_miner import RefactoringMiner
from get_commit_diff import process_commit_diff


FILE_NAME = "./data/sonar_measures.csv"
JSON_FILE_PATH = "./output"

print('----------------------------------')
print(os.getcwd())
print('----------------------------------')
# instance of CSVHandler
csv_handler = CSVHandler(FILE_NAME)

# instance of refactoring miner
refactoring_miner = RefactoringMiner()

# read the csv file
rows = csv_handler.read_csv()

# get project name column
all_projects = csv_handler.get_project_name_column(rows)
print('All projects are: ', all_projects)
print('Total projects are: ', len(all_projects))

# format project names
# formatted_projects = csv_handler.format_project_name(all_projects)

# get unique projects
# unique_projects = csv_handler.get_unique_projects(formatted_projects)
# print('Unique projects are: ', unique_projects)
# print('Total unique projects are: ', len(unique_projects))

# write unique projects to a csv file
# csv_handler.write_json(unique_projects, 'unique_projects.json')

# build the github url for the projects
# unique_projects_url = csv_handler.build_github_url(unique_projects)

# write the unique projects url to a json file
# csv_handler.write_json(unique_projects_url, 'unique_projects_url.json')

# cloning repositories -> data is stored in the cloned_repos folder
# csv_handler.clone_repo(unique_projects_url)

# getting the local repo names
local_repo_name = csv_handler.local_repo_name()
# print(local_repo_name)

# get project all commit hashes
project_commit_hashes = refactoring_miner.get_all_commits(local_repo_name)
csv_handler.write_json(project_commit_hashes, 'project_commit_hashes.json')

# split the project commit hashes
split_project_commit_hashes = refactoring_miner.split_commits_into_batches(project_commit_hashes, 500)
# print('Split project commit hashes are: ', split_project_commit_hashes)
csv_handler.write_json(split_project_commit_hashes, 'split_project_commit_hashes.json')

# run refactoring miner
refactoring_miner.get_refactorings(split_project_commit_hashes)

# analyze each json file to get the project data to work with
csv_handler.merge_json_files_by_project_and_cleanup()

# parse the json files and creates the refactoring_commits folder
csv_handler.parse_json_files()

# get refactoring types and save to a json file
refactoring_miner.get_refactoring_types("./refactoring_commits")

# get the commit hash
commits_hash = refactoring_miner.get_commits_hash("./refactoring_commits")
# csv_handler.write_json(commits_hash, 'commits_hash.json')

# get interefactoring commit period from commit hash (actual mining)
interefactoring_commit_period = refactoring_miner.get_interefactoring_commit_period('./commits_hash')

# get the average time between commits
refactoring_miner.get_average_time_between_refactorings('./interefactoring_commit_period')

# get commit diff
process_commit_diff('./commits_hash')

