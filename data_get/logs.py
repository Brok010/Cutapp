# makes a simple text file each time the gui is set.

import os
import datetime
import json

from gui import ProjectProperties_dic, MainBoard_dic, Saw_dic, Cuts_list

# finds how many files with th same/similar name/date was created
def find_files(folderpath, formattedtime):
    count = 0
    filesindir = os.listdir(folderpath)
    for filename in filesindir:
        if formattedtime in filename:
            count += 1
    return count

# make a string of a dict
def dic_to_str(dic):
    str_dic = json.dumps(dic)
    return str_dic

# if the folder does not exist yet, create one
Folder_Name = 'Logs'
Current_Dir = os.getcwd()
Folder_Path = os.path.join(Current_Dir, Folder_Name)
if not os.path.exists(Folder_Path):
    os.mkdir(Folder_Path)

# text file name gen
CurrentTime = datetime.datetime.now()
FormattedTime = CurrentTime.strftime('%Y.%m.%d.')

# check for existing files with similar name
FileCount = find_files(Folder_Path, FormattedTime)
FileName = FormattedTime + str(FileCount + 1) + '.txt'
File_Path = os.path.join(Folder_Path, FileName)

# create the log    
with open(File_Path, 'w') as file:
    file.write('Project properties: ' + dic_to_str(ProjectProperties_dic) + '\n')
    file.write('Main board: ' + dic_to_str(MainBoard_dic) + '\n')
    file.write('Saw: ' + dic_to_str(Saw_dic) + '\n')
    for each in Cuts_list:
        file.write('Cut: ' + dic_to_str(each) + '\n')