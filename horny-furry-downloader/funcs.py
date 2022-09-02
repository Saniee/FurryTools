import os
from time import sleep
from urllib.parse import urlparse
import requests
import pathlib

def getAllPosts(urls, head):
    posts = []
    for u in urls:
        postID = urlparse(u).__getattribute__('path')[1:].split('/')[1]
        body = requests.get(f"https://e621.net/posts.json?tags=id:{postID}", headers=head)
        p = body.json()
        posts.append(p['posts'][0])
        sleep(0.2)
    return posts

def download(url, id, artist, head, count):
    file_ext = pathlib.Path(url).suffix
    fileRequest = requests.get(url, headers=head)

    if (os.path.exists(os.getcwd()+f'./download/{artist} - {id}{file_ext}') == True):
        print(f'File - {artist} - {id}{file_ext} already exists!')
        return 0
    else: 
        print(f'Downloading {artist} - {id}{file_ext}!')
        with open(f'./download/{artist} - {id}{file_ext}', 'wb') as f:
                    f.write(fileRequest.content)

def readFile(file):
    urls = file.readlines()
    return urls