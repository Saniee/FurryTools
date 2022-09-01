from ctypes import Array
import os
from tkinter import filedialog

dirpath = filedialog.askdirectory(initialdir=os.getcwd())

if dirpath == '':
    exit()


def bulkrename(fileList: Array):
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

    print('\n')
    return renameCount, deleteCount


list_of_files = os.listdir(dirpath)
Count = bulkrename(list_of_files)
print('Running again, for checking SPOILERname occurences!\n')
list_of_files = os.listdir(dirpath)
NewCount = bulkrename(list_of_files)
print('Renamed {} Files and Removed {} Files! Exiting...'.format(Count[0] + NewCount[0], Count[1] + NewCount[1]))
