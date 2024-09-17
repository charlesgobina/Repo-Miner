import subprocess
import os
import shutil
from get_github_url import CSVHandler

pwd = os.getcwd()


refactoring_miner_path = f"{pwd}/tools/RefactoringMiner/cmd-tool/RefactoringMiner-3.0.7/bin"

print(f"Current working directory: {refactoring_miner_path}");
print(pwd)


class RefactoringMiner:
  def __init__(self):
    pass
  
  def get_refactorings(self, github_repos):
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
      subprocess.run(["./RefactoringMiner", "-a", github_repo_path, "-json", f"{pwd}/output/{github_repo}.json"])  
  

  
# refac = RefactoringMiner()

# refac.get_refactorings()