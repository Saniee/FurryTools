import os
import tkinter as tk
from tkinter import filedialog

def start():
    dirpath = filedialog.askdirectory(initialdir=os.getcwd())
    
    if dirpath == '':
        exit()

    fileList = os.listdir(dirpath)

    renameCount = 0
    deleteCount = 0
    for filename in fileList:
        if 'SPOILER_' in filename:
            newName = filename.replace('SPOILER_', '')
            newNamePath = dirpath + '/' + newName
            if os.path.exists(newNamePath):
                deleteCount += 1
                os.remove(dirpath + '/' + filename)
                print("Dealt with a duplicated File! {} was removed.".format(filename))
            else:
                renameCount += 1
                os.rename(dirpath + '/' + filename, newNamePath)
                print("Renamed {} to {} | File number: {}".format(filename, newName, renameCount))
        elif 'SPOILER' in filename:
            newName = filename.replace('SPOILER', '')
            newNamePath = dirpath + '/' + newName
            if os.path.exists(newNamePath):
                deleteCount += 1
                os.remove(dirpath + '/' + filename)
                print("Dealt with a duplicated File. {} was removed.".format(filename))

            else:
                renameCount += 1
                os.rename(dirpath + '/' + filename, newNamePath)
                print("Renamed {} to {} | File number: {}".format(filename, newName, renameCount))