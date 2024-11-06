'''
TBW'''
import os
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
formatted_projects = csv_handler.format_project_name(all_projects)

# get unique projects
unique_projects = csv_handler.get_unique_projects(formatted_projects)
print('Unique projects are: ', unique_projects)
print('Total unique projects are: ', len(unique_projects))

# build the github url for the projects
# unique_projects_url = csv_handler.build_github_url(unique_projects)

# cloning repositories -> data is stored in the cloned_repos folder
# csv_handler.clone_repo(unique_projects_url)

# getting the local repo names
# local_repo_name = csv_handler.local_repo_name()
# print(local_repo_name)

# using refactoring miner on the repositories
# refactoring_miner.get_refactorings(local_repo_name)

# analyze each json file to get the project data to work with
json_data = csv_handler.parse_json_files()

# get refactoring types and save to a json file
refactoring_types = refactoring_miner.get_refactoring_types(json_data)
csv_handler.write_json(refactoring_types, 'refactoring_types.json')

# get the commit hash
commits_hash = refactoring_miner.get_commits_hash(json_data)
csv_handler.write_json(commits_hash, 'commits_hash.json')

# get interefactoring commit period from commit hash (actual mining)
interefactoring_commit_period = refactoring_miner.get_interefactoring_commit_period(commits_hash)
csv_handler.write_json(interefactoring_commit_period, 'interefactoring_commit_period.json')

# get the interefactoring commit period
interefactoring_commit_period = csv_handler.read_json('interefactoring_commit_period.json')

# get the average time between commits
time_between_commits = refactoring_miner.get_average_time_between_refactorings(interefactoring_commit_period)
csv_handler.write_json(time_between_commits, 'time_between_commits.json')

# get commit diff
commit_diff = process_commit_diff('commits_hash.json')
# print('Commit diff is: ', commit_diff)
# write commit diff to a json file
csv_handler.write_json(commit_diff, 'commit_diff.json')
