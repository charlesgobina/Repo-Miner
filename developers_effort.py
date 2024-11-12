"""Developers effort component: collects total TLOC for each refactoring and developer"""

import os
import json
from operator import itemgetter
from pprint import pprint
import subprocess
from configparser import ConfigParser
import git


class DevEffort:
    """Class for developers effort; initialized with a GitHub project path"""

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

    def filter_programming_languages(self, scc_file):
        """Removes non-programming languages using the TIOBE index"""
        # filtered_data = []

        with open(scc_file, 'r', encoding='utf-8') as file:
            scc_data = json.load(file)

            # Filter out non-programming languages
            for entry in scc_data:
                language = entry.get("Name")
                if language not in self.tiobe_index:
                    scc_data.remove(entry)

        # filtered_scc_file = f"filtered_{scc_file}"
        # Save the filtered data to a new JSON file
        with open(scc_file, 'w', encoding='utf-8') as filtered_scc_file:
            json.dump(scc_data, filtered_scc_file, indent=4)

        print(f"Filtered data saved to {scc_file}")

    def get_loc(self, project, output_directory, commit, is_refactoring):
        """Switches current repository to specified commit"""
        subprocess.run(["git", "checkout", f"{commit}"], check=False)
        scc_directory = f"{output_directory}{self.config['output']['path'][1:]}/{project}/scc"
        if not os.path.exists(scc_directory):
            os.mkdir(scc_directory)

        if is_refactoring:
            scc_file = f"{scc_directory}/refactoring_{commit}.json"
        else:
            scc_file = f"{scc_directory}/commit_{commit}.json"
        subprocess.run(["scc", "-f", "json", "-o", scc_file], check=False)

        print(scc_file)

        self.filter_programming_languages(scc_file)

        loc_counter = 0
        with open(scc_file, 'r', encoding='utf-8') as file:
            scc_data = json.load(file)
            for language in scc_data:
                loc = language['Code']
                loc_counter += loc

        print(loc_counter)
        return loc_counter

    def touched_lines_of_code(self, current_dir, project_dir, project_name, commit_details_list):
        """Gets the touched lines of code for each commit of a project"""

        output_directory = os.getcwd()

        tloc_list = []
        os.chdir(project_dir)
        for commit in commit_details_list:
            commit_hash = commit['commit_hash']
            current_loc = self.get_loc(
                project_name, output_directory, commit_hash, 1)

            rev_parse_command = subprocess.check_output(
                ["git", "rev-parse", f"{commit_hash}^1"])
            previous_commit = rev_parse_command.decode('utf-8').strip()
            previous_loc = self.get_loc(
                project_name, output_directory, previous_commit, 0)

            tloc = abs(current_loc - previous_loc)
            tloc_list.append(tloc)

        # for tloc in tloc_list:
        #     print(tloc)

        os.chdir(current_dir)

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

            commit_details_list = self.collect_commit_details(
                project, project_repo)
            sorted_commit_details = sorted(
                commit_details_list, key=itemgetter('date'))

            output_dir = f"{self.config['output']['path']}/{project_name}"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            cd_file = f"{output_dir}/commit_details.json"
            with open(cd_file, 'w', encoding='utf-8') as cd_file:
                json.dump(sorted_commit_details, cd_file)

            pretty_print = 0
            if pretty_print:
                pprint(sorted_commit_details)
            # print(len(sorted_commit_details))

            cwd = os.getcwd()
            self.touched_lines_of_code(
                cwd, project_dir, project_name, sorted_commit_details)
