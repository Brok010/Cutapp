import os
from datetime import datetime
import subprocess
import json

from objects import Board, Saw, Cut

#get input from Logs
folder_path = 'Logs'
debug_file_path = 'Logs/debug.txt'

#check if there is a debug file
if os.path.isfile(debug_file_path):
    with open(debug_file_path, 'r') as f:
        file_content = f.readlines()
# else create a new file and run it
else:
    subprocess.run(['python', 'logs.py'])
    files_in_folder = os.listdir(folder_path)
    #check for right format
    date_format = "%Y.%m.%d"
    filtered_files = [file for file in files_in_folder if len(file) >= len("yyyy.mm.dd.x") and file.count('.') == 4]
    sorted_files = sorted(filtered_files, key=lambda file: int(file[11:-4]))
    # load last file
    if sorted_files:
        latest_file = sorted_files[-1]
        latest_file_path = os.path.join(folder_path, latest_file)
        with open(latest_file_path, 'r') as f:
            file_content = f.readlines()        

# load data from text file into variables
MainBoard = Board()
CurrentSaw = Saw()
Cuts = []
for line in file_content:
    if 'Project properties' in line:
        ProjectProperties = json.loads(line.split('Project properties: ')[-1])
    elif 'Main board' in line:
        MainBoard_dic = json.loads(line.split('Main board: ')[-1])
        MainBoard.label = MainBoard_dic['Label']
        MainBoard.real_valueX = MainBoard_dic['Real_valueX']
        MainBoard.real_valueY = MainBoard_dic['Real_valueY']
        MainBoard.real_valueZ = MainBoard_dic['Real_valueZ']
        MainBoard.notes = MainBoard_dic['Notes']
        MainBoard.generate = MainBoard_dic['Generate']
        MainBoard.direction = MainBoard_dic['Direction']
    elif 'Saw' in line:
        CurrentSaw_dic = json.loads(line.split('Saw: ')[-1])
        CurrentSaw.label = CurrentSaw_dic['Label']
        CurrentSaw.real_valueX = CurrentSaw_dic['Real_valueX']
        CurrentSaw.notes = CurrentSaw_dic['Notes']
        CurrentSaw.generate = CurrentSaw_dic['Generate']
    elif 'Cut' in line:
        CurrentCut = Cut()
        Cut_dic = json.loads(line.split('Cut: ')[-1])
        CurrentCut.label = Cut_dic['Label']
        CurrentCut.real_valueX = Cut_dic['Real_valueX']
        CurrentCut.real_valueY = Cut_dic['Real_valueY']
        CurrentCut.notes = Cut_dic['Notes']
        CurrentCut.generate = Cut_dic['Generate']
        CurrentCut.direction = Cut_dic['Direction']
        CurrentCut.count = Cut_dic['Count']
        Cuts.append(CurrentCut)

# remove cuts that are not real
if len(Cuts) > 1:
    for i in range(len(Cuts), 1, -1):
        if Cuts[i - 1].real_valueX <= 0 or Cuts[i - 1].real_valueY <= 0:
            Cuts.remove(Cuts[i - 1])
elif Cuts[0].real_valueX <= 0 or Cuts[0].real_valueY <= 0:
    Cuts.remove(Cuts[0])