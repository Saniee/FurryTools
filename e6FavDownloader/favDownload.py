from inspect import ArgSpec
import os
import requests
import threading

import funcs

name = input('Enter the Username of whom you will download theyere favs: ')

url = f'https://e621.net/posts.json?tags=fav:{name}'

if (os.path.isdir(os.getcwd()+"/download") != True):
    os.mkdir(os.getcwd()+f"/download")

head = {'User-Agent': 'favDownloader/0.1'}

body = requests.get(url, headers=head)
posts = body.json()

i = 0

favsCount = len(posts['posts'])

print(f'Downloading {favsCount} favs!')

while i < len(posts['posts']):
    fileUrl = posts['posts'][i]['file']['url']
    artistArray = posts['posts'][i]['tags']['artist']
    postID = posts['posts'][i]['id']
    artistName = ''

    if (len(artistArray) > 1):
        for a in artistArray:
            artistName = artistName + f'{a}, '
    else:
        artistName = artistArray = posts['posts'][i]['tags']['artist'][0]

    threading.Thread(target=funcs.download, args=(fileUrl, artistName, postID, head)).start()

    i = i + 1
