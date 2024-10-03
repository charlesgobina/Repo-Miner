import json
from fileinput import close

import jsonpickle

from pydriller import repository, Repository, Git

class diffFile:
    fileName = '';
    addedLines = 0;
    deletedLines = 0;
    diff = '';
    def __init__(self, fileName, addedLines, deletedLines, diff):
        self.fileName = fileName;
        self.addedLines = addedLines;
        self.deletedLines = deletedLines;
        self.diff = diff;

class commitInfo:
    commitId = '';
    parentCommitId = '';
    diffChange = [];
    def __init__(self, commitId, parentcommitId, diffChange):
        self.diffChange = diffChange;
        self.commitId = commitId;
        self.parentCommitId = parentcommitId;

class projectInfo:
    projectName = ''
    commits = []
    def __init__(self, projectName, commits):
        self.projectName = projectName
        self.commits = commits

f = open("commits_hash.json", "r");
data1 = json.load(f);
projectList = [];
for key in data1:
    print("Project: " + key.get('project'))
    gr = Git('repository/' + key.get('project'))
    commitList = [];
    for commitId in key.get('commits'):
        #print(' Commit: ' + commitId);
        commit = gr.get_commit(commitId);
        parentCommitId = ''
        for parentCommit in commit.parents:
            #print('     Parent commit: ' + parentCommit)
            parentCommitId = parentCommit;
        #print("     Deletion: " + str(commit.deletions));
        listDiff = [];
        for file in (commit.modified_files):
            listDiff.append(diffFile(file.filename, file.added_lines, file.deleted_lines, ''));
            # print('         File change: ' + file.filename);
            # print('         Added lines: ' + str(file.added_lines))
            # print('         Deleted lines: ' + str(file.deleted_lines));
        commitList.append(commitInfo(commitId, parentCommitId, listDiff))
    projectList.append(projectInfo(key.get('project'), commitList))


jsonStr = jsonpickle.encode(projectList);
#jsonsTr2 = json.encoder(projectList);
f2 = open("output.json","w+")
#f2.write(jsonsTr2)
print("Object:")
print(projectList[1]);
f2.close();
print(jsonStr)




# print(data1)
# gr = Git('iotdb');
# commit = gr.get_commit('0137093279915f59a83fd46354b1b44de27c74cf');
# for str1 in commit.parents:
#     print('parent commit:' + str1);
# print(commit.deletions);
#
# for file in (commit.modified_files):
#     print('file changes:' + file.filename);
#     print('added:' + str(file.added_lines));
#     print('deleted:' + str(file.deleted_lines));

print("done");

