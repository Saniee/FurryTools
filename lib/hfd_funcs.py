import os
from time import sleep
from urllib.parse import urlparse
import requests
import pathlib

from PIL import ImageTk, Image
from io import BytesIO


def getAllPosts(urls, head, nsfw):
    posts = []
    for u in urls:
        postID = urlparse(u).__getattribute__('path')[1:].split('/')[1]

        if (nsfw):
            url = f"https://e621.net/posts.json?tags=id:{postID}"
        else:
            url = f"https://e926.net/posts.json?tags=id:{postID}"

        body = requests.get(url, headers=head)
        p = body.json()
        if (len(p['posts']) != 0):
            posts.append(p['posts'][0])
            sleep(0.2)
    return posts


def download(url, id, artist, head, d, viewWindowImg):
    file_ext = pathlib.Path(url).suffix
    fileRequest = requests.get(url, headers=head)

    if (os.path.exists(d + f'/{artist} - {id}{file_ext}') == True):
        print(f'File - {artist} - {id}{file_ext} already exists!')
        return 0
    else:
        print(f'Downloaded {artist} - {id}{file_ext}!')
        with open(d + f'/{artist} - {id}{file_ext}', 'wb') as f:
            f.write(fileRequest.content)

    if (file_ext == ".jpg" or file_ext == ".png" or file_ext == ".gif"):
        img = ImageTk.PhotoImage(Image.open(
            BytesIO(fileRequest.content)).resize((750, 750), Image.ANTIALIAS))
        viewWindowImg.configure(image=img)
        viewWindowImg.image = img


def readFile(file):
    urls = file.readlines()
    return urls
