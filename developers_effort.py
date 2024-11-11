"""Developers effort component: collects total TLOC for each refactoring and developer"""

import os
import json
from operator import itemgetter
from pprint import pprint
import subprocess
import git
from configparser import ConfigParser

class DevEffort:
    """Class for developers effort; initialized with a GitHub project path"""

    commit_details_matrix = []

    def __init__(self, json_path, config: ConfigParser):

        self.config = config
        # print(f"Reading JSON file: {json_path}")
        self.json_path = json_path
        # print(self.get_json())

    def get_json(self):
        """Goes through the projects inside the JSON"""
        with open(self.json_path, encoding="utf-8") as file:
            json_data = json.load(file)
        return json_data

    def get_project_dir(self, project):
        """Returns project directory"""
        project_path = f"{self.config['path']['project_path'] + '/' + project}"
        return project_path

    def collect_commit_details(self, project, project_repo):
        """Collects commit details: hash, author, date, lines changed, files changed"""
        commit_details_list = []
        # print(project_dir)
        for commit_hash in project["commits"]:
            # print(commit_hash)
            # print(project_repo)
            commit = project_repo.commit(commit_hash)
            try:
                commit = project_repo.commit(commit_hash)
                commit_details = {
                    "commit_hash": commit_hash,
                    "author": commit.author.name,
                    "date": commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")
                }
                commit_details_list.append(commit_details)

            except ValueError as value_error:
                print(
                    f"Warning: Commit {commit_hash} could not be resolved. Skipping.")
                print(f"Value Error: {value_error}")
                return None
        return commit_details_list

    def get_loc(self, directory, commit):
        """Switches current repository to specified commit"""
        
        subprocess.run(["git", "checkout", f"{commit}"], check=False)
        scc_file = f"scc_{commit}.json"
        subprocess.run(["scc", "-f", "json", "-o", scc_file], check=False)

        loc_counter = 0
        with open(scc_file, 'r', encoding='utf-8') as scc_file:
            scc_data = json.load(scc_file)
            for language in scc_data:
                loc = language['Code']
                loc_counter += loc
        # print(loc_counter)
        return loc

    def touched_lines_of_code(self, current_directory, project_dir, commit_details_list):
        """Gets the touched lines of code for each commit of a project"""

        tloc_list = []
        os.chdir(project_dir)
        for commit in commit_details_list:
            commit_hash = commit['commit_hash']          
            current_loc = self.get_loc(project_dir, commit_hash)

            rev_parse_command = subprocess.check_output(["git", "rev-parse", f"{commit_hash}^1"])
            previous_commit = rev_parse_command.decode('utf-8').strip()
            previous_loc = self.get_loc(project_dir, previous_commit)

            tloc = abs(current_loc - previous_loc)
            tloc_list.append(tloc)

        for tloc in tloc_list:
            print(tloc)

        os.chdir(current_directory)

    def mine_projects(self):
        """Prints commit data"""
        json_data = self.get_json()
        # print(json_data)

        projects = []

        for project in enumerate(json_data):
            projects.append({
                "index": project[0],
                "project": project[1]["project"],
                "commits": project[1]["commits"]
            })

        for project in projects:
            # print(project["project"])
            project_name = project["project"]
            project_dir = self.get_project_dir(project_name)
            project_repo = git.Repo(project_dir)

            commit_details_list = self.collect_commit_details(project, project_repo)
            sorted_commit_details = sorted(commit_details_list, key=itemgetter('date'))

            with open(f"{self.config['output']['path'] + '/' + project_name + '/' + 'commit_details.json'}", 'w', encoding='utf-8') as cd_file:
                json.dump(sorted_commit_details, cd_file)

            pretty_print = 1
            if pretty_print:
                pprint(sorted_commit_details)
            # print(len(sorted_commit_details))

            current_directory = os.getcwd()
            self.touched_lines_of_code(current_directory, project_dir, sorted_commit_details)
