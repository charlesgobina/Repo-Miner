# importing csv module
import csv
import requests
import subprocess
import os
import json

# csv file name
filename = "./data/sonar_measures.csv"
cloned_repos_path = "./cloned_repos"


class CSVHandler:
    def __init__(self, filename):
        self.filename = filename
    
    def read_csv(self):
        rows = []
        with open(self.filename, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            # extracting each data row one by one
            for row in csvreader:
                rows.append(row)
        return rows
    
    def get_project_name_column(self, rows):
        all_projects = []
        for row in rows:
            # parsing each column of a row
            for col in row[1:2]:
                all_projects.append(col)
        return all_projects
    
    def format_project_name(self, project_list):
        formatted_project_list = []
        for project in project_list:
            formatted_project = project[7:]
            formatted_project_list.append(formatted_project)
        return formatted_project_list
     
    def get_unique_projects(self, project_list):
        return list(set(project_list))
    
    def build_github_url(self, unique_projects):
        unique_project_urls = [] # list to store unique project urls
        for project in unique_projects:
            project_url = f"https://github.com/apache/{project}"
            unique_project_urls.append(project_url)
        return unique_project_urls
    
    def clone_repo(self, unique_project_urls):
        repo_names = []
        for project_url in unique_project_urls:
            # use subprocess to clone the repository
            subprocess.run(["git", "clone", project_url, f"{cloned_repos_path}/{project_url.split('/')[-1]}"])
            # store the name of the repos
        #     repo_names.append(project_url.split('/')[-1])
        #     print(repo_names)
        # return repo_names 

    def local_repo_name(self):
        cloned_repos_path = "./cloned_repos"
        folders = [name for name in os.listdir(cloned_repos_path) if os.path.isdir(os.path.join(cloned_repos_path, name))]
        return folders
    
    
    def get_repo_info(self, unique_projects):
        # GitHub API endpoint for getting the languages of a repository
        url = f"https://api.github.com/repos/apache/{unique_projects[300]}/languages"
        response = requests.get(url)
        if response.status_code == 200:
            languages = response.json()  # The response is a JSON object
            print("Languages used in the repository:")
            for language, bytes_of_code in languages.items():
              print(f"{language}: {bytes_of_code} bytes")
        else:
            print('Failed!')
    
    def parse_json_files(str:dir):
      print(f"Processing JSON files in {dir}")
      json_data = []

      # Iterate through all files in the directory
      for filename in os.listdir(dir):
          if filename.endswith(".json"):  # Process only .json files
              file_path = os.path.join(dir, filename)
              print(f"Processing {file_path}")
              
              # Open and parse the JSON file
              with open(file_path, 'r') as file:
                  data = json.load(file)
                  
                  # Append the list data from the JSON file to json_data
                  if isinstance(data, list):  # Ensure data is a list
                      json_data.append(data)
                  else:
                      print(f"Data in {filename} is not a list")

      return json_data
      
