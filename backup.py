"""Developers effort component: collects total TLOC for each refactoring and developer"""

import os
import json
from operator import itemgetter
from pprint import pprint
import subprocess
import git
from configparser import ConfigParser
import pandas as pd



pwd_original = os.getcwd()


class DevEffort:
    """Class for developers effort; initialized with a directory containing JSON files"""

    tiobe_index = {
        "Visual FoxPro", "1C", "4th Dimension", "ABAP", "ABC", "ActionScript", "Ada",
        "Agilent VEE", "Algol", "Alice", "Angelscript", "Apex", "APL", "Applescript",
        "Arc", "AspectJ", "Assembly language", "ATLAS", "AutoHotkey", "AutoIt", "AutoLISP",
        "Awk", "Bash", "Basic", "bc", "BCPL", "BETA", "Bourne shell", "Brainfuck", "C shell",
        "C#", "C++", "C", "Caml", "Carbon", "Ceylon", "CFML", "Chapel", "CHILL", "CIL",
        "Clojure", "COBOL", "CoffeeScript", "Crystal", "Curl", "D", "Dart", "Delphi/Object Pascal",
        "DiBOL", "Dylan", "E", "ECMAScript", "Eiffel", "Elixir", "Elm", "Emacs Lisp", "Erlang",
        "F#", "Factor", "Falcon", "Fantom", "Forth", "Fortran", "FreeBASIC", "GAMS", "GLSL",
        "Go", "Groovy", "Hack", "Harbour", "Haskell", "Haxe", "Heron", "Icon", "IDL", "Idris",
        "Io", "J", "JADE", "Java", "JavaScript", "Julia", "Korn shell", "Kotlin", "LabVIEW",
        "Ladder Logic", "Lasso", "Lingo", "Lisp", "Logo", "LotusScript", "Lua", "MAD", "Magic",
        "Magik", "MANTIS", "Maple", "MATLAB", "Max/MSP", "MAXScript", "MEL", "Mercury", "ML",
        "Modula-2", "Modula-3", "Monkey", "MQL5", "MS-DOS batch", "MUMPS", "NATURAL", "Nim",
        "NQC", "Objective-C", "OCaml", "OpenCL", "OpenEdge ABL", "OPL", "Oz", "Pascal", "Perl",
        "PHP", "Pike", "PostScript", "PowerBasic", "PowerShell", "Processing", "Prolog",
        "PureBasic", "Python", "R", "Racket", "REBOL", "Red", "REXX", "Ring", "RPG", "Ruby",
        "Rust", "SAS", "Scala", "Scheme", "sed", "Seed7", "Simula", "Simulink", "Smalltalk",
        "Smarty", "Solidity", "SPARK", "SPSS", "SQL", "SQR", "Squirrel", "Standard ML", "Stata",
        "Swift", "SystemVerilog", "Tcl", "Transact-SQL", "TypeScript", "Uniface", "Vala/Genie",
        "VBScript", "VHDL", "Visual Basic", "WebAssembly", "Wolfram", "X++", "X10", "XBase",
        "XBase++", "XC", "Xen", "Xojo", "XQuery", "XSLT", "Xtend", "Z shell", "Zig"
    }

    commit_details_matrix = []

    def __init__(self, json_dir, config: ConfigParser):
        self.json_dir = json_dir

    def get_json_files(self):
        """Returns a list of JSON files in the directory"""

        # loop through the directory and get project name from directory
        for project in os.listdir(self.json_dir):
            project_name = project.split(".")[0]
            if (project_name == "sling-org-apache-sling-commons-log-webconsole"):
                print("_____________________________________")
                print(f"Project name: {project_name} \n")
                print("_____________________________________")
            else:
                print(f"Project name: {project_name} \n")
            if not os.path.exists(f"{pwd_original}/developer_effort/{project_name}"):
                os.makedirs(f"{os.getcwd()}/developer_effort/{project_name}")
        return [f for f in os.listdir(self.json_dir) if f.endswith('.json')]

    def get_json(self, json_file):
        """Reads a JSON file and returns its content"""
        with open(os.path.join(self.json_dir, json_file), encoding="utf-8") as file:
            json_data = json.load(file)
        return json_data

    def get_project_dir(self, project):
        """Returns project directory"""
        pwd = os.getcwd()
        project_path = f"{pwd}/cloned_repos/{project}"
        return project_path

    def collect_commit_details(self, project, project_repo):
        """Collects commit details: hash, author, date, lines changed, files changed"""
        commit_details_list = []
        for commit_hash in project["commits"]:
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

    def filter_programming_languages(self, scc_file):
        """Removes non-programming languages using the TIOBE index"""
        # filtered_data = []

        with open(scc_file, 'r', encoding='utf-8') as file:
            scc_data = json.load(file)

            # Filter out non-programming languages
            for index, entry in enumerate(scc_data):
                language = entry.get("Name")
                if language not in self.tiobe_index:
                    # delete the entire entry
                    del scc_data[index]
        # filtered_scc_file = f"filtered_{scc_file}"
        # Save the filtered data to a new JSON file
        with open(scc_file, 'w', encoding='utf-8') as filtered_scc_file:
            json.dump(scc_data, filtered_scc_file, indent=4)

        print(f"Filtered data saved to {scc_file}")
    
    def effort_by_developer(self, project_name):
        """Organizes the scc output by developer"""
        output_dir = f"{self.config['output']['path']}/{project_name}"

        commit_details_file = f"{output_dir}/commit_details.json"
        dev_dir = f"{output_dir}"
        if not os.path.exists(dev_dir):
            os.makedirs(dev_dir)

        with open(commit_details_file, 'r', encoding='utf-8') as file:
            commit_data = json.load(file)

        # print(f"\033[91m{commit_data}\033[00m")

        csv_file = pd.read_csv(f"{self.config['output']['path']}/{project_name}/dev_effort.csv")

        # Process the data to get the output
        dev_list = {}
        for commit in commit_data:
            dev = commit['author']
            target_hash = commit['commit_hash']
            tloc_result = csv_file.loc[csv_file['refactoring_hash'] == target_hash, 'TLOC']

            if not tloc_result.empty:
                tloc_value = int(tloc_result.iloc[0])
                if dev in dev_list:
                    dev_list[dev] += tloc_value
                else:
                    dev_list[dev] = tloc_value
            else:
                print("No matching row found for refactoring hash: ", target_hash)

        # print(f"\033[91m{dev_list}\033[00m")

        # Write the output data to a new JSON file
        dev_file = f"{dev_dir}/dev.json"
        with open(dev_file, 'w', encoding='utf-8') as file:
            json.dump(dev_list, file, indent=4)

        # print(f"\033[91mOutput has been written to {dev_file}\033[00m")

    def get_loc(self, directory, commit):
        """Switches current repository to specified commit"""
        project_name = directory.split("/")[-1]

        print("''''''''''''''''''''''''''''")
        print("Project name: ", f'{project_name} \n')
        print("''''''''''''''''''''''''''''")

        if not os.path.exists(f"{pwd_original}/developer_effort/{project_name}"):
            os.makedirs(f"{os.getcwd()}/developer_effort/{project_name}")

        os.chdir(directory)

        subprocess.run(["git", "checkout", f"{commit}"], check=False)
        scc_file = f"scc_{commit}.json"
        subprocess.run(["scc", "-f", "json", "-o",
                        f'{pwd_original}/developer_effort/{project_name}/{scc_file}'], check=False)

        os.chdir(f"{pwd_original}/developer_effort/{project_name}")
        # filter the programming languages
        self.filter_programming_languages(scc_file)
        loc_counter = 0
        with open(scc_file, 'r', encoding='utf-8') as scc_file:
            scc_data = json.load(scc_file)
            for language in scc_data:
                loc = language['Code']
                loc_counter += loc
        return loc

    def touched_lines_of_code(self, current_directory, project_dir, commit_details_list):
        """Gets the touched lines of code for each commit of a project"""
        tloc_list = []

        for commit in commit_details_list:
            commit_hash = commit['commit_hash']

            print("Commit hash: ", commit_hash)
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
            print(tloc)

        os.chdir(pwd_original)

    def mine_projects(self):
        """Processes each JSON file in the directory and prints commit data"""
        json_files = self.get_json_files()
        print(json_files)

        for json_file in json_files:
            json_data = self.get_json(json_file)
            projects = []

            for project in enumerate(json_data):
                projects.append({
                    "index": project[0],
                    "project": project[1]["project"],
                    "commits": project[1]["commits"]
                })

            for project in projects:
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
                self.effort_by_developer(project_name)
