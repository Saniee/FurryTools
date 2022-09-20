from re import T
import threading
from urllib.parse import urlparse
import os
import requests

import tkinter as tk
from tkinter import filedialog

from lib import hfd_funcs as funcs
from tools import search as srch


def start(app, nsfw):
    window = tk.Toplevel(app)
    window.geometry('425x350')
    window.resizable(0, 0)

    LSearch = tk.Label(window, text="Search for posts with tags and download them:")
    LSearch.pack()

    searchLabel = tk.Label(window, text="Set Tags to search")
    searchLabel.pack()
    searchEntry = tk.Entry(window)
    searchEntry.pack()
    limitLabel = tk.Label(window, text="Set amount which to download")
    limitLabel.pack()
    limitEntry = tk.Entry(window)
    limitEntry.pack()
    runBtn = tk.Button(window, text="Search & Download!", command= lambda: runSearch(searchEntry.get(), limitEntry.get(), nsfw))
    runBtn.pack()

    spacerL = tk.Label(window)
    spacerL.pack()

    LPostDw = tk.Label(window, text="Download with urls:")
    LPostDw.pack()

    L1 = tk.Label(window, text="Input a url without anything else then the ID (https://e926.net/posts/XXXXXXX)")
    L1.pack()
    inp = tk.Entry(window)
    inp.pack()
    setFileBtn = tk.Button(window, command= lambda: getTxtPath(inp) ,text="Click to get a txt file with urls instead")
    setFileBtn.pack()
    L3 = tk.Label(window, text="Click to set the download directory.")
    L3.pack()
    dirBtn = tk.Button(window, command= lambda: getDirPath(dirLabel), text="Set directory!")
    dirBtn.pack()
    dirLabelTxt = tk.Label(window, text="Downloading to:")
    dirLabelTxt.pack()
    dirLabel = tk.Label(window, text=f"{os.getcwd()}")
    dirLabel.pack()
    runBtn = tk.Button(window, command= lambda: runUrl(inp.get(), dirLabel["text"]), text="Download!")
    runBtn.pack()

    def runSearch(i, limit, nsfw):
        if (nsfw):
            url = f"https://e621.net/posts.json?tags={i}&limit={limit}"
        else:
            url = f"https://e926.net/posts.json?tags={i}&limit={limit}"
        
        head = {'User-Agent': 'FurryTools/0.5'}

        posts = requests.get(url, headers=head)
        p = posts.json()

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

    def getDirPath(label):
        d = filedialog.askdirectory(initialdir=os.getcwd())
        label.configure(text=d)
    
    def getTxtPath(entry):
        d = filedialog.askopenfilename(initialdir=os.getcwd())
        entry.insert(0, d)

    def runUrl(i, d):
        count = 0
        head = {'User-Agent': 'FurryTools/0.5'}
        if (os.path.exists(os.path.dirname(i))):
            file = open(i, 'r')
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
