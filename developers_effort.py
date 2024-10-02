"""Developers effort component: collects total TLOC for each refactoring and developer"""

import json
from pprint import pprint
import git


class DevEffort:
    """Class for developers effort; initialized with a GitHub project path"""

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

    def collect_commit_details(self):
        """Collects commit details: hash, author, date, lines changed, files changed"""
        json_data = self.get_json()
        # print(json_data)

        projects = []
        commit_details_matrix = []

        for project in enumerate(json_data):
            projects.append({
                "index": project[0],
                "project": project[1]["project"],
                "commits": project[1]["commits"]
            })
        # projects.reverse()

        for project in projects:
            print(project["project"])
            project_dir = self.get_project_dir(project["project"])
            project_repo = git.Repo(project_dir)
            commit_details_list = []
            # print(project_dir)
            for commit_hash in project["commits"]:
                # print(commit_hash)
                # print(project_repo)
                commit = project_repo.commit(commit_hash)
                try:
                    commit = project_repo.commit(commit_hash)
                    commit_details = {
                        "project": project['project'],
                        "commit_hash": commit_hash,
                        "author": commit.author.name,
                        # "date": commit.committed_datetime,
                        "lines_changed": commit.stats.total['lines'],
                        "files_changed": len(commit.stats.files)
                    }
                    commit_details_list.append(commit_details)

                except ValueError as value_error:
                    print(
                        f"Warning: Commit {commit_hash} could not be resolved. Skipping.")
                    print(f"Value Error: {value_error}")
                    return None
                commit_details_matrix.append(commit_details_list)
        return commit_details_matrix

    def print_commit_data(self):
        """Prints commit data"""
        commit_details_list = self.collect_commit_details()
        # pprint(commit_details_list)
        print(len(commit_details_list))

        with open('commit_details.json', 'w', encoding='utf-8') as cd_file:
            json.dump(commit_details_list, cd_file)

        return cd_file

    def organize_by_refactoring(self):
        """Organizes the output by refactoring"""

    def organize_by_developer(self):
        """Organizes the output by developer"""
