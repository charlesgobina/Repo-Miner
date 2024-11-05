'''
TBW'''
import subprocess
import os
from datetime import datetime
from pydriller import Repository
from github import Github
from github import Auth

auth = Auth.Token('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')
pwd = os.getcwd()
g = Github(auth=auth)


refactoring_miner_path = f"{pwd}/tools/RefactoringMiner/cmd-tool/RefactoringMiner-3.0.7/bin"

print(f"Current working directory: {refactoring_miner_path}")
print(pwd)


class RefactoringMiner:
    '''
    Class to mine refactoring data from the cloned repositories'''
    def __init__(self):
        pass

    def get_refactorings(self, github_repos):
        '''
        TBW'''
        # use subprocess to run RefactoringMiner on the cloned repositories
        if os.getcwd() != refactoring_miner_path:
            os.chdir(refactoring_miner_path)
        for github_repo in github_repos:
            # check if github_repo actually exists
            if github_repo not in os.listdir(f"{pwd}/cloned_repos"):
                print(f"Repository {github_repo} does not exist")
                continue
            else:
                print(f"Repository {github_repo} exists")
                print(os.getcwd())
            print(f"Running RefactoringMiner on {github_repo}")
            github_repo_path = f"{pwd}/cloned_repos/{github_repo}"
            # path to the cloned repository
            subprocess.run(["./RefactoringMiner",
                            "-a",
                            github_repo_path,
                            "-json",
                            f"{pwd}/output/{github_repo}.json"], check=False)

    def get_refactoring_types(self, refactoring_data):
        '''
        TBW
        '''
        refactoring_types = []
        for index_ref, refactoring in enumerate(refactoring_data):
            refactoring_types.append(
                {
                    "project": refactoring['project'],
                    "refactoring_type": [],
                    "count_per_type": {}
                })
            for index, ref in enumerate(refactoring["commits_data"]):
                print(index)
                if len(ref["refactorings"]) != 0:
                    for ref_type in ref["refactorings"]:
                        refactoring_types[index_ref]["refactoring_type"].append(
                            ref_type['type'])
        # make the refactoring types unique
        for refac in refactoring_types:
            refac["count_per_type"] = {ref_type: refac["refactoring_type"].count(
                ref_type) for ref_type in refac["refactoring_type"]}
            refac["refactoring_type"] = list(set(refac["refactoring_type"]))

        return refactoring_types

    def get_commits_hash(self, refactoring_data):
        '''
        TBW
        '''
        commits_hash = []
        for index, refactoring in enumerate(refactoring_data):
            commits_hash.append(
                {
                    "project": refactoring['project'],
                    "commits": []
                })
            for ref in refactoring["commits_data"]:
                commits_hash[index]["commits"].append(ref["commit_hash"])
        return commits_hash

    def get_interefactoring_commit_period(self, commits_hash):
        '''
        TBW
        '''
        repo_data = []

        for index, commits in enumerate(commits_hash):
            # get the name of the repository
            repo = g.get_repo(f"apache/{commits['project']}")
            repo_data.append({
                "project": commits['project'],
                "commits": []
            })
            for commit in commits['commits']:
                # get the commit period
                commit_period = repo.get_commit(commit).commit.author.date
                repo_data[index]['commits'].append({
                    "commit_hash": commit,
                    "commit_period": commit_period
                })
        # convert datetime to string in the repo_data
        for repo in repo_data:
            for commit in repo['commits']:
                commit['commit_period'] = commit['commit_period'].strftime(
                    "%Y-%m-%d %H:%M:%S")
        return repo_data

    def get_average_time_between_refactorings(self, refactoring_data):
        '''
        TBW
        '''
        commit_time_diff = []
        for index, refactoring in enumerate(refactoring_data):
            commit_time_diff.append({
                "project": refactoring['project'],
                "commits_diff": [],
                "average_time_between_refactorings": 0,
            })
            for commit in refactoring['commits']:
                commit['commit_period'] = datetime.strptime(
                    commit['commit_period'], "%Y-%m-%d %H:%M:%S")
            for i in range(1, len(refactoring['commits'])):
                time_diff = refactoring['commits'][i]['commit_period'] - refactoring['commits'][i-1]['commit_period']
                # convert all negative time_diff to positive with absoulte
                # time_diff = abs(time_diff)
                # convert time_diff to string
                # time_diff = str(time_diff)
                # convert time_diff to seconds
                time_diff = time_diff.total_seconds()
                time_diff = abs(time_diff)
                commit_time_diff[index]['commits_diff'].append(time_diff)
        # add key for average time between refactorings
        for index, refactoring in enumerate(commit_time_diff):
            print(commit_time_diff[index])
            commit_time_diff[index]['average_time_between_refactorings'] = sum(
                refactoring['commits_diff']) / len(refactoring['commits_diff'])
            # convert average time between refactorings to days
            commit_time_diff[index]['average_time_between_refactorings_in_days'] = commit_time_diff[index]['average_time_between_refactorings'] / 86400
        return commit_time_diff

        # get the name of the repository
        # for index, commits in enumerate(commits_hash):
        #     repo_name = commits['project']
        #     # format the repository name
        #     repo_name = repo_name.split('/')[-1]
        #     if repo_name in os.listdir(f"{pwd}/cloned_repos"):
        #         repo_path = f"{pwd}/cloned_repos/{repo_name}"
        #         repo_data.append(
        #             {
        #                 "project": repo_name,
        #                 "path": repo_path,
        #                 "commits": []
        #             }
        #         )
        #         # get the commits
        #         print(f"Getting commits for {repo_name}")
        #         print(f"Repository path: {repo_path}")
        #         repo = Repository(repo_path)

        #         for commit in repo.traverse_commits():
        #             if commit.hash in commits['commits']:
        #                 print(commit.hash, commit.author.name, commit.author.email, commit.msg)
        #                 # get the commit period
        #                 commit_period = commit.committer_date
        #                 print(commit_period)
        #                 repo_data[index]['commits'].append({
        #                     "commit_hash": commit.hash,
        #                     "commit_period": commit_period
        #                 })

        # # convert datetime to string in the repo_data
        # for repo in repo_data:
        #     for commit in repo['commits']:
        #         commit['commit_period'] = commit['commit_period'].strftime("%Y-%m-%d %H:%M:%S")

        # return repo_data

# refac = RefactoringMiner()

# refac.get_refactorings()
