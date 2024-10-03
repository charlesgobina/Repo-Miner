from get_github_url import CSVHandler
from refactoring_miner import RefactoringMiner
from pydriller import Commit


filename = "./data/sonar_measures.csv"
json_files_path = "./output"

# instance of CSVHandler
csv_handler = CSVHandler(filename)

# instance of refactoring miner
refactoring_miner = RefactoringMiner()

# read the csv file
rows = csv_handler.read_csv()

# get project name column
all_projects = csv_handler.get_project_name_column(rows)
# print('All projects are: ', all_projects)
print('Total projects are: ', len(all_projects))

# format project names
formatted_projects = csv_handler.format_project_name(all_projects)

# get unique projects
unique_projects = csv_handler.get_unique_projects(formatted_projects)
# print('Unique projects are: ', unique_projects)
print('Total unique projects are: ', len(unique_projects))

# build github url
# unique_projects_url = csv_handler.build_github_url(unique_projects)
# print('Unique projects urls are: \n', unique_projects_url)

# clone repo
# csv_handler.clone_repo(unique_projects_url)
# add logic to clone repo if the cloned_repos directory does not exist /
# is empty

# local_repo_name = csv_handler.local_repo_name()

# print(local_repo_name)

# using refactoring miner on the repositories
# refactoring_miner.get_refactorings(local_repo_name)

# analyze each json file to get the data
json_data = csv_handler.parse_json_files('./output')

# get refactoring types
refactoring_types = refactoring_miner.get_refactoring_types(json_data)
# print(json_data[0])

# save the refactoring types to a json file
# csv_handler.write_json(refactoring_types, 'refactoring_types.json')

# get commit hash
# commits_hash = refactoring_miner.get_commits_hash(json_data)

# csv_handler.write_json(commits_hash, 'commits_hash.json')

# get interefactoring commit period
# interefactoring_commit_period = refactoring_miner.get_interefactoring_commit_period(commits_hash)
# print(interefactoring_commit_period)

# get the time between commits from json file
interefactoring_commit_period = csv_handler.read_json('interefactoring_commit_period.json')


time_between_commits = refactoring_miner.get_average_time_between_refactorings(interefactoring_commit_period)
# csv_handler.write_json(interefactoring_commit_period, 'interefactoring_commit_period.json')
print(time_between_commits)
csv_handler.write_json(time_between_commits, 'time_between_commits.json')
# print('Refactoring types are: ', refactoring_types)
