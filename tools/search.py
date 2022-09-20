import tkinter as tk
from tkinter import filedialog
import requests
import os

import threading
from urllib.parse import urlparse

from lib import hfd_funcs as funcs

def run(window, nsfw):
    newWin = tk.Toplevel(window)
    newWin.geometry('250x200')
    newWin.resizable(0, 0)
    
    searchLabel = tk.Label(newWin, text="Set Tags to search")
    searchLabel.pack()
    searchEntry = tk.Entry(newWin)
    searchEntry.pack()
    limitLabel = tk.Label(newWin, text="Set amount which to download")
    limitLabel.pack()
    limitEntry = tk.Entry(newWin)
    limitEntry.pack()
    runBtn = tk.Button(newWin, text="Search!", command= lambda: runSearch(searchEntry.get(), limitEntry.get(), nsfw))
    runBtn.pack()

    def runSearch(i, limit, nsfw):
        if (nsfw):
            url = f"https://e621.net/posts.json?tags={i}&limit={limit}"
        else:
            url = f"https://e926.net/posts.json?tags={i}&limit={limit}"
        
        head = {'User-Agent': 'FurryTools/0.5'}

        posts = requests.get(url, headers=head)
        p = posts.json()
        L1 = tk.Label(newWin, text=f"Found {len(p['posts'])} posts!")
        L1.pack()
        L2 = tk.Label(newWin, text="Downloading...")
        L2.pack()

        count = 0

        d = filedialog.askdirectory(initialdir=os.getcwd())

        while count < len(p['posts']):
            fileUrl = p['posts'][count]['file']['url']
            artistArray = p['posts'][count]['tags']['artist']
            postID = p['posts'][count]['id']
            artistName = ''

            if (len(artistArray) > 1):
                for a in artistArray:
                    artistName = artistName + f'{a}, '
                artistName = artistName[:-2]
            elif(len(p['posts'][count]['tags']['artist']) != 0):
                artistName = p['posts'][count]['tags']['artist'][0]
            else:
                artistName = 'unknown'

            threading.Thread(target=funcs.download, args=(
                fileUrl, artistName, postID, head, d)).start()

            count += 1

