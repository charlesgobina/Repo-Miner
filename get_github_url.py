'''
TBW
'''
import subprocess
import os
import json
# import requests
import csv

# csv file name
# filename = "./data/sonar_measures.csv"


class CSVHandler:
    '''
    Class to handle CSV files'''
    def __init__(self, filename_i):
        self.filename = filename_i

    def read_csv(self):
        '''
        Read a CSV file'''
        rows = []
        with open(self.filename, 'r', encoding="utf-8") as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            # extracting each data row one by one
            for row in csvreader:
                rows.append(row)
        return rows

    def write_json(self, data, filename_j):
        '''
        Write data to a JSON file'''
        with open(filename_j, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def read_json(self, filename_j):
        '''
        Read a JSON file'''
        with open(filename_j, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def get_project_name_column(self, rows):
        '''
        Get the project name column from the csv file'''
        all_projects = []
        for row in rows:
            # parsing each column of a row
            for col in row[1:2]:
                all_projects.append(col)
        return all_projects

    def format_project_name(self, project_list):
        '''
        Format the project names'''
        formatted_project_list = []
        for project in project_list:
            formatted_project = project[7:]
            formatted_project_list.append(formatted_project)
        return formatted_project_list

    def get_unique_projects(self, project_list):
        '''
        Get the unique projects'''
        return list(set(project_list))

    def build_github_url(self, unique_projects):
        '''
        Build the GitHub URL for the projects'''
        unique_project_urls = []  # list to store unique project urls
        # limit the number of projects to 5
        unique_projects = unique_projects[:5]
        for project in unique_projects:
            project_url = f"https://github.com/apache/{project}"
            unique_project_urls.append(project_url)
        return unique_project_urls

    # add logic to ask the user where they want to clone the repos
    def clone_repo(self, unique_project_urls):
        '''
        Clone the repositories'''
        cloned_repos_path = "./cloned_repos"
        repo_names = []
        for project_url in unique_project_urls:
            if project_url == "https://github.com/apache/":
                continue
            # use subprocess to clone the repository
            subprocess.run(["git", "clone", project_url,
                           f"{cloned_repos_path}/{project_url.split('/')[-1]}"], check=True)
            # store the name of the repos
            repo_names.append(project_url.split('/')[-1])
            print(repo_names)
        return repo_names

    def local_repo_name(self):
        '''
        Get the names of the cloned repositories
        '''
        cloned_repos_path = "./cloned_repos"
        folders = [
            name for name in os.listdir(cloned_repos_path) if os.path.isdir(
                os.path.join(
                    cloned_repos_path,
                    name))]
        return folders

    # def get_repo_info(self, unique_projects):
    #     # GitHub API endpoint for getting the languages of a repository
    #     url = f"https://api.github.com/repos/apache/{unique_projects[300]}/languages"
    #     response = requests.get(url, timeout=5)
    #     if response.status_code == 200:
    #         languages = response.json()  # The response is a JSON object
    #         print("Languages used in the repository:")
    #         for language, bytes_of_code in languages.items():
    #             print(f"{language}: {bytes_of_code} bytes")
    #     else:
    #         print('Failed!')

    def parse_json_files(self, directory: str):
        '''
        Parse JSON files in a directory'''
        print(f"Processing JSON files in {directory}")
        json_data = []
        mined_commit_data = []

        # Iterate through all files in the directory
        for proc_filename in os.listdir(directory):
            if proc_filename.endswith(".json"):  # Process only .json files
                file_path = os.path.join(
                    os.path.abspath(directory), proc_filename)
                print(f"Processing {file_path}")

                # Open and parse the JSON file
                with open(file_path, 'r', encoding="utf-8") as file:
                    data = json.load(file)

                    data = data['commits']

                    # Append the list data from the JSON file to json_data
                    if isinstance(data, list):  # Ensure data is a list
                        json_data.append(data)
                        non_empty_commit_data = []

                        for datum in data:
                            if len(datum['refactorings']) != 0:
                                non_empty_commit_data.append(
                                    {
                                        "commit_hash": datum['sha1'],
                                        "refactorings": datum['refactorings']
                                    }
                                )
                        mined_commit_data.append(
                            {"project": proc_filename.split(
                                ".")[0], "commits_data": non_empty_commit_data}
                        )
                    else:
                        print(f"Data in {proc_filename} is not a list")
        # Write the mined commit data to a JSON file
        self.write_json(mined_commit_data, 'mined_commit_data.json')
        return mined_commit_data
