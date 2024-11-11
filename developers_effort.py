"""Developers effort component: collects total TLOC for each refactoring and developer"""

import os
import json
from operator import itemgetter
from pprint import pprint
import subprocess
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
        # get the current working directory
        pwd = os.getcwd()
        project_path = f"{pwd}/cloned_repos/{project}"
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

        # get project name from directory
        project_name = directory.split("/")[-1]

        pwd_original = os.getcwd()
        if not os.path.exists(f"{os.getcwd()}/developer_effort/{project_name}"):
            os.makedirs(f"{os.getcwd()}/developer_effort/{project_name}")

        os.chdir(directory)

        subprocess.run(["git", "checkout", f"{commit}"], check=False)
        scc_file = f"scc_{commit}.json"
        subprocess.run(["scc", "-f", "json", "-o",
                       f'{pwd_original}/developer_effort/{project_name}/{scc_file}'], check=False)

        os.chdir(f"{pwd_original}/developer_effort/{project_name}")
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

        print("-------------------------------------------------")
        print(current_directory)
        print(project_dir)
        print("-------------------------------------------------")  

        for commit in commit_details_list:
            commit_hash = commit['commit_hash']

            print("Commit hash: ", commit_hash)
            print(commit_hash)
            current_loc = self.get_loc(project_dir, commit_hash)

            try:
                rev_parse_command = subprocess.check_output(
                    ["git", "rev-parse", f"{commit_hash}^1"], stderr=subprocess.STDOUT)
                previous_commit = rev_parse_command.decode('utf-8').strip()
                previous_loc = self.get_loc(project_dir, previous_commit)
                tloc = abs(current_loc - previous_loc)
            except subprocess.CalledProcessError as e:
                print(
                    f"Error getting previous commit for {commit_hash}: {e.output.decode('utf-8')}")
                tloc = current_loc  # If there's no previous commit, consider the current LOC as TLOC

            tloc_list.append(tloc)

        for tloc in tloc_list:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(tloc)

        print(current_directory)
        os.chdir(current_directory)

    def mine_projects(self):
        """Prints commit data"""
        json_data = self.get_json()
        # print(json_data)
        print("###########################___________________")
        print(os.getcwd())
        print("###########################___________________")

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
            print(project_dir)
            project_repo = git.Repo(project_dir)

            commit_details_list = self.collect_commit_details(
                project, project_repo)
            sorted_commit_details = sorted(
                commit_details_list, key=itemgetter('date'))

            with open(f"{os.getcwd()}/developer_effort/{project_name}.json", 'w', encoding='utf-8') as cd_file:
                json.dump(sorted_commit_details, cd_file, indent=4)

            print("############################################")
            print("Commit details for project: ", sorted_commit_details)

            pretty_print = 0
            if pretty_print:
                pprint(sorted_commit_details)
            print(len(sorted_commit_details))

            current_directory = os.getcwd()
            self.touched_lines_of_code(
                current_directory, project_dir, sorted_commit_details)
