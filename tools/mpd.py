from re import T
import threading
from urllib.parse import urlparse
import os
import requests

import tkinter as tk
from tkinter import filedialog

from lib import hfd_funcs as funcs

head = {'User-Agent': 'FurryTools/0.7'}


def runSearch(i, limit, nsfw, viewWindowImg):
    if (nsfw):
        url = f"https://e621.net/posts.json?tags={i}&limit={limit}"
    else:
        url = f"https://e926.net/posts.json?tags={i}&limit={limit}"

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
        elif (len(p['posts'][count]['tags']['artist']) != 0):
            artistName = p['posts'][count]['tags']['artist'][0]
        else:
            artistName = 'unknown'

        threading.Thread(target=funcs.download, args=(
            fileUrl, artistName, postID, head, d, viewWindowImg)).start()

        count += 1


def getDirPath(label):
    d = filedialog.askdirectory(initialdir=os.getcwd())
    label.configure(text=d)


def getTxtPath(entry):
    d = filedialog.askopenfilename(initialdir=os.getcwd())
    entry.insert(0, d)


def runUrl(i, d, nsfw, viewWindowImg):
    count = 0
    if (os.path.exists(os.path.dirname(i))):
        file = open(i, 'r')
        urls = funcs.readFile(file)
        print(f'Getting all the data!')
        posts = funcs.getAllPosts(urls, head, nsfw)
        if (len(posts) != 0):
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
                elif (len(posts[count]['tags']['artist']) != 0):
                    artistName = posts[count]['tags']['artist'][0]
                else:
                    artistName = 'unknown'
                threading.Thread(target=funcs.download, args=(
                    fileUrl, postID, artistName, head, d, viewWindowImg)).start()
                count += 1
        elif (len(posts) != 0 & nsfw):
            print(f'The list either has only nsfw posts or an error happened.')
        else:
            print(f"There is nothing to download")
    else:
        postID = urlparse(i).__getattribute__('path')[1:].split('/')[1]
        if (nsfw):
            url = f"https://e621.net/posts.json?tags=id:{postID}"
        else:
            url = f"https://e926.net/posts.json?tags=id:{postID}"
        post = requests.get(
            url, headers=head)
        p = post.json()
        artistArray = p['posts'][0]['tags']['artist']
        artistName = ''
        if (len(artistArray) > 1):
            for a in artistArray:
                artistName = artistName + f'{a}, '
                artistName = artistName[:-2]
        elif (len(p['posts'][0]['tags']['artist']) != 0):
            artistName = p['posts'][0]['tags']['artist'][0]
        else:
            artistName = 'unknown'

        funcs.download(p['posts'][0]['file']['url'],
                       postID, artistName, head, d, viewWindowImg)
