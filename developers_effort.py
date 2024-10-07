"""Developers effort component: collects total TLOC for each refactoring and developer"""

import json
from pprint import pprint
import datetime
import subprocess
import os
import git

class DevEffort:
    """Class for developers effort; initialized with a GitHub project path"""

    commit_details_matrix = []

    def __init__(self, json_path):
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
        project_path = f"/home/taba/root/projects/{project}"
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
                    # "project": project['project'],
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
        commit_details_list.reverse()
        return commit_details_list

    def touched_lines_of_code(self, current_directory, project_dir, commit_details_list):
        """Gets the touched lines of code for each commit of a project"""
        first_commit = 1
        counter = 0
        tloc_list = []
        for commit in commit_details_list:
            commit_hash = commit['commit_hash']
            # print(f"Commit Hash: {commit_hash}")

            os.chdir(project_dir)
            checkout_command = subprocess.run(["git", "checkout", f"{commit_hash}"], check=False)
            # print(checkout_command)
            scc_command = subprocess.run(["scc", "-f", "json", "-o", "scc.json"], check=False)

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

            pretty_print = 0
            if pretty_print:
                pprint(commit_details_list)
            # print(len(commit_details_list))

            with open(f"commit_details/{project_name}.json", 'w', encoding='utf-8') as cd_file:
                json.dump(commit_details_list, cd_file)

            current_directory = os.getcwd()
            self.touched_lines_of_code(current_directory, project_dir, commit_details_list)
