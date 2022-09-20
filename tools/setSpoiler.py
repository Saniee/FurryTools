import os
import tkinter
from tkinter import filedialog

def start():
    dirpath = filedialog.askdirectory(initialdir=os.getcwd())

    if dirpath == '':
        return

    listDir = os.listdir(dirpath)

    renameCount = 0
    filename: str;
    for (filename) in listDir:
        renameCount += 1
        newName = ("SPOILER_" + filename)
        newNamePath = dirpath + '/' + newName
        os.rename(dirpath + '/' + filename, newNamePath)
        print("Renamed {} to {} | File number: {}".format(filename, newName, renameCount))