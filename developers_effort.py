"""Developers effort component: collects total TLOC for each refactoring and developer"""

import json


class DevEffort:
    """Class for developers effort; initialized with a GitHub project path"""

    def __init__(self, json_path):
        self.json_path = json_path

    def get_json(self):
        """Goes through the projects inside the JSON"""
        with open(self.json_path, encoding="utf-8") as file:
            json_data = json.load(file)
        return json_data
        
    def collect_commit_details(self, json_data):
        """Collects commit details: hash, author, date, lines changed, files changed"""
        projects = []
        for index, commit_hash in enumerate(json_data):
            projects.append({
                "project": commit_hash["project"],
                "commit_details": []
            })
            for commit in commit_hash["commits"]:



        try:
            commit = project.commit(commit_hash)
            commit_details = {
                "commit_hash": commit_hash,
                "author": commit.author.name,
                "date": commit.committed_datetime,
                "lines_changed": commit.stats.total['lines'],
                "files_changed": len(commit.stats.files)
            }
            return commit_details
        except ValueError as value_error:
            print(f"Warning: Commit {commit_hash} could not be resolved. Skipping.")
            print(f"Value Error: {value_error}")
            return None

    def print_commit_data(self):
        """Prints commit data"""
        for project in self.get_json():
            print(f"Project: {project['project']}")
            for commit_hash in project['commits']:
                details = self.collect_commit_details(commit_hash)
                if details:
                    print(f"Commit: {commit_hash}")
                    print(f"Author: {details['author']}, Date: {details['date']}")
                    print(f"Lines Changed: {details['lines_changed']}")
                    print(f"Files Changed: {details['files_changed']}")
                    print("-" * 40)

# INPUT: repository name and commit hashes
# go inside local repository
# pydriller
# get author name
# SCC: touched lines of code for each developer
