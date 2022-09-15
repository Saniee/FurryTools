from tools import fv
from tools import hfd

from tools import setSpoiler
from tools import removeSpoiler

import tkinter as tk

app = tk.Tk()
app.geometry("300x150")
app.title('ETools')
app.resizable(0, 0)

fd_button = tk.Button(app, command= lambda: fv.start(app), text="Favorite Download")
fd_button.pack()

hfd_button = tk.Button(app, command= lambda: hfd.start(app), text="Mass Post/Post Downloader")
hfd_button.pack()

addSp = tk.Button(app, command= lambda: setSpoiler.start(), text="Add Spoiler tags")
addSp.pack()

remSp = tk.Button(app, command= lambda: removeSpoiler.start(), text="Remove Spoiler tags")
remSp.pack()

l1 = tk.Label(app, text="Made by Saniee")
l1.pack(side=tk.BOTTOM)

if __name__ == "__main__":
    app.mainloop()