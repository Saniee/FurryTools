import os

from tools import fv
from tools import mpd

from tools import setSpoiler
from tools import removeSpoiler

import tkinter as tk

app = tk.Tk()
# app.geometry("1000x500")
app.title('FurryTools')
app.resizable(0, 0)

nsfwMPD = tk.BooleanVar()
nsfwFV = tk.BooleanVar()
nsfwTag = tk.BooleanVar()

""" addSp = tk.Button(app, command= lambda: setSpoiler.start(), text="Add Spoiler tags")
addSp.grid()

remSp = tk.Button(app, command= lambda: removeSpoiler.start(), text="Remove Spoiler tags")
remSp.grid() """

# w425 x h350
mpdFrame = tk.Frame(app, width=250, height=250)
mpdFrame.grid(row=0, column=0)

viewWindow = tk.Toplevel(app)

viewWindow.geometry('750x750')
viewWindow.title('IMG Viewer')
viewWindowImg = tk.Label(viewWindow)
viewWindowImg.pack(side="bottom", fill="both", expand="yes")

siteCheckbox = tk.Checkbutton(
    mpdFrame, text="Download NSFW?", variable=nsfwMPD, onvalue=True, offvalue=False)
siteCheckbox.grid()

HFDL1 = tk.Label(
    mpdFrame, text="Input a url without anything else then the ID (https://e926.net/posts/XXXXXXX)")
HFDL1.grid()
inp = tk.Entry(mpdFrame)
inp.grid()
setFileBtn = tk.Button(mpdFrame, command=lambda: mpd.getTxtPath(
    inp), text="Click to get a txt file with urls instead")
setFileBtn.grid()
HFDL3 = tk.Label(mpdFrame, text="Click to set the download directory.")
HFDL3.grid()
dirBtn = tk.Button(mpdFrame, command=lambda: mpd.getDirPath(
    dirLabel), text="Set directory!")
dirBtn.grid()
dirLabelTxt = tk.Label(mpdFrame, text="Downloading to:")
dirLabelTxt.grid()
dirLabel = tk.Label(mpdFrame, text=f"{os.getcwd()}")
dirLabel.grid()
runBtn = tk.Button(mpdFrame, command=lambda: mpd.runUrl(
    inp.get(), dirLabel["text"], nsfwMPD.get(), viewWindowImg), text="Download!")
runBtn.grid()

tagSearchFrame = tk.Frame(app, width=250, height=250)
tagSearchFrame.grid(row=0, column=1)

siteCheckboxFV = tk.Checkbutton(
    tagSearchFrame, text="Download NSFW?", variable=nsfwTag, onvalue=True, offvalue=False)
siteCheckboxFV.grid()

searchLabel = tk.Label(tagSearchFrame, text="Set Tags to search")
searchLabel.grid()
searchEntry = tk.Entry(tagSearchFrame)
searchEntry.grid()
limitLabel = tk.Label(tagSearchFrame, text="Set amount which to download")
limitLabel.grid()
limitEntry = tk.Entry(tagSearchFrame)
limitEntry.grid()
runBtn = tk.Button(tagSearchFrame, text="Search & Download!", command=lambda: mpd.runSearch(
    searchEntry.get(), limitEntry.get(), nsfwTag.get(), viewWindowImg))
runBtn.grid()

fvFrame = tk.Frame(app, width=250, height=250)
fvFrame.grid(row=0, column=2)

siteCheckboxFV = tk.Checkbutton(
    fvFrame, text="Download NSFW?", variable=nsfwFV, onvalue=True, offvalue=False)
siteCheckboxFV.grid()

L1 = tk.Label(fvFrame, text="Input the Username")
L1.grid()
nameInput = tk.Entry(master=fvFrame)
nameInput.grid()
# input('Enter the Username of whom you will download theyere favs: ')
L2 = tk.Label(fvFrame, text="Input how much favorites you want. (320 Max)")
L2.grid()
limitInput = tk.Entry(master=fvFrame)
limitInput.grid()
# input('Enter how much favorites you want to download (MAX is 320): ')
runBtn = tk.Button(master=fvFrame, command=lambda: fv.run(
    nameInput.get(), limitInput.get(), nsfwFV.get(), viewWindowImg), text="Download!")
runBtn.grid()

if __name__ == "__main__":
    app.mainloop()
