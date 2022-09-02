import threading
from tkinter import filedialog
from urllib.parse import urlparse
import os
import requests

import funcs

i = input('Enter Url or type in `file` here: ')

count = 0

head = {'User-Agent': 'HornyFurryDownloader-HFD/0.1'}

if (os.path.isdir(os.getcwd()+"/download") != True):
    os.mkdir(os.getcwd()+f"/download")

if (i == "file"):
    file = filedialog.askopenfile(initialdir=os.getcwd(), filetypes=[('Text Files', '*.txt')])
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
            fileUrl, postID, artistName, head, count)).start()
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

    funcs.download(p['posts'][0]['file']['url'], postID, artistName, head)