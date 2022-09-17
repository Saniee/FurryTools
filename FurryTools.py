from tools import fv
from tools import hfd

from tools import setSpoiler
from tools import removeSpoiler

import tkinter as tk

app = tk.Tk()
app.geometry("300x200")
app.title('ETools')
app.resizable(0, 0)

nsfw = tk.BooleanVar()

siteCheckbox = tk.Checkbutton(app, text="NSFW?", variable=nsfw, onvalue=True, offvalue=False)
siteCheckbox.pack()

fd_button = tk.Button(app, command= lambda: fv.start(app, nsfw.get()), text="Favorite Download")
fd_button.pack()

hfd_button = tk.Button(app, command= lambda: hfd.start(app, nsfw.get()), text="Mass Post/Post Downloader")
hfd_button.pack()

addSp = tk.Button(app, command= lambda: setSpoiler.start(), text="Add Spoiler tags")
addSp.pack()

remSp = tk.Button(app, command= lambda: removeSpoiler.start(), text="Remove Spoiler tags")
remSp.pack()

l2 = tk.Label(app, text="Made by Saniee")
l2.pack(side=tk.BOTTOM)

if __name__ == "__main__":
    app.mainloop()