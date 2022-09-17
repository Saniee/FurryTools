import threading
from tkinter import filedialog
from urllib.parse import urlparse
import os
import requests

import tkinter as tk
from tkinter import filedialog

from lib import hfd_funcs as funcs


def start(app, nsfw):
    Window = tk.Toplevel(app)
    Window.geometry('300x200')
    Window.title('Horny Furry Downloader')
    Window.resizable(0, 0)
    L1 = tk.Label(Window, text="Input a url without anything else then the ID")
    L1.pack()
    L2 = tk.Label(Window, text="Example: https://e926.net/posts/XXXXXXXX")
    L2.pack()
    L3 = tk.Label(Window, text="Leave blank for getting posts from a file.")
    L3.pack()
    inp = tk.Entry(Window)
    inp.pack()
    L4 = tk.Label(Window, text="Click to set the download directory.")
    L4.pack()
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
            posts = funcs.getAllPosts(urls, head, nsfw)
            if(len(posts) != 0):
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
                    elif(len(posts[count]['tags']['artist']) != 0):
                        artistName = posts[count]['tags']['artist'][0]
                    else:
                        artistName = 'unknown'
                    threading.Thread(target=funcs.download, args=(
                        fileUrl, postID, artistName, head, d)).start()
                    count += 1
            elif(len(posts) != 0 & nsfw): 
                print(f'The list either has only nsfw posts or an error happened.')
            else:
                print(f"There is nothing to download")
        else:
            if (nsfw):
                url = f"https://e621.net/posts.json?tags=id:{postID}"
            else:
                url = f"https://e926.net/posts.json?tags=id:{postID}"

            postID = urlparse(i).__getattribute__('path')[1:].split('/')[1]
            post = requests.get(
                url, headers=head)
            p = post.json()
            artistArray = p['posts'][0]['tags']['artist']
            artistName = ''
            if (len(artistArray) > 1):
                for a in artistArray:
                    artistName = artistName + f'{a}, '
                    artistName = artistName[:-2]
            elif(len(p['posts'][0]['tags']['artist']) != 0):
                artistName = p['posts'][0]['tags']['artist'][0]
            else:
                artistName = 'unknown'
        
            funcs.download(p['posts'][0]['file']['url'], postID, artistName, head, d)
