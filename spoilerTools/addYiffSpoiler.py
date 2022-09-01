import os
from tkinter import filedialog

dirpath = filedialog.askdirectory(initialdir=os.getcwd())

def addSpoiler(listDir):
    renameCount = 0
    filename: str;
    for (filename) in listDir:
        renameCount += 1
        newName = ("SPOILER_" + filename)
        newNamePath = dirpath + '/' + newName
        os.rename(dirpath + '/' + filename, newNamePath)
        print("Renamed {} to {} | File number: {}".format(filename, newName, renameCount))

    return renameCount

list = os.listdir(dirpath)
count = addSpoiler(list)
print('Renamed {} files!'.format(count))