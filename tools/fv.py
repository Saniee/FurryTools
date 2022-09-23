import requests
import threading
import os

import tkinter as tk
from tkinter import filedialog

from lib import f_funcs as funcs

head = {'User-Agent': 'FurryTools/0.6'}


def run(name, limit, nsfw):
    d = filedialog.askdirectory(initialdir=os.getcwd())

    if (int(limit) > 320):
        print('I am sorry but the hard limit is 320.')
        print('Running again...')

    if (nsfw):
        url = f'https://e621.net/posts.json?tags=fav:{name}&limit={limit}'
    else:
        url = f'https://e926.net/posts.json?tags=fav:{name}&limit={limit}'

    body = requests.get(url, headers=head)
    p = body.json()

    if (body.status_code == 403):
        print(f'The user {name} has blocked access to theyre favorites.')
        print('Running again...')

    i = 0

    favsCount = len(p['posts'])

    print(f'Downloading {favsCount} favs!')

    while i < len(p['posts']):
        fileUrl = p['posts'][i]['file']['url']
        artistArray = p['posts'][i]['tags']['artist']
        postID = p['posts'][i]['id']
        artistName = ''

        if (len(artistArray) > 1):
            for a in artistArray:
                artistName = artistName + f'{a}, '
            artistName = artistName[:-2]
        elif (len(p['posts'][i]['tags']['artist']) != 0):
            artistName = p['posts'][i]['tags']['artist'][0]
        else:
            artistName = 'unknown'

        threading.Thread(target=funcs.download, args=(
            fileUrl, artistName, postID, head, d)).start()

        i = i + 1
