import threading
from tkinter import filedialog
from urllib.parse import urlparse
import os
import requests

import tkinter as tk
from tkinter import filedialog

from lib import hfd_funcs as funcs


def start(app):
    Window = tk.Toplevel(app)
    Window.geometry('500x200')
    Window.title('Horny Furry Downloader')
    L1 = tk.Label(Window, text="Input a url without anything else then the ID")
    L1.pack()
    L2 = tk.Label(Window, text="Example: https://e621.net/posts/XXXXXXXX")
    L2.pack()
    inp = tk.Entry(Window)
    inp.pack()
    L3 = tk.Label(Window, text="Click to set the download directory.")
    L3.pack()
    dirBtn = tk.Button(Window, command= lambda: getDirPath(dirLabel), text="Set directory!")
    dirBtn.pack()
    dirLabelTxt = tk.Label(Window, text="Downloading to:")
    dirLabelTxt.pack()
    dirLabel = tk.Label(Window)
    dirLabel.pack()
    runBtn = tk.Button(Window, command= lambda: run(inp.get(), dirLabel["text"]), text="Download!")
    runBtn.pack()

    def getDirPath(label):
        d = filedialog.askdirectory(initialdir=os.getcwd())
        label.configure(text=d)

    def run(i, d):
        count = 0

        head = {'User-Agent': 'HornyFurryDownloader-HFD/0.1'}
        if (i == ""):
            file = filedialog.askopenfile(initialdir=os.getcwd(), filetypes=[
                ('Text Files', '*.txt')])
            urls = funcs.readFile(file)
            print(f'Getting all the data!')
            posts = funcs.getAllPosts(urls, head)
            print(f'Downloading {len(posts)} posts!')
            while count < len(urls):
                fileUrl = posts[count]['file']['url']
                postID = posts[count]['id']
                artistArray = posts[count]['tags']['artist']
                artistName = ''
                if (len(artistArray) > 1):
                    for a in artistArray:
                        artistName = artistName + f'{a}, '
                    artistName = artistName[:-1]
                else:
                    artistName = artistArray = posts[count]['tags']['artist'][0]
                threading.Thread(target=funcs.download, args=(
                    fileUrl, postID, artistName, head, d)).start()
                count += 1
        else:
            postID = urlparse(i).__getattribute__('path')[1:].split('/')[1]
            post = requests.get(
                f"https://e621.net/posts.json?tags=id:{postID}", headers=head)
            p = post.json()
            artistArray = p['posts'][0]['tags']['artist']
            artistName = ''
            if (len(artistArray) > 1):
                for a in artistArray:
                    artistName = artistName + f'{a}, '
                    artistName = artistName[:-1]
            else:
                artistName = artistArray = p['posts'][0]['tags']['artist'][0]
        
            funcs.download(p['posts'][0]['file']['url'], postID, artistName, head, d)
