import os
from urllib.parse import urlparse
import requests
import pathlib
from clint.textui import progress

head = {'User-Agent': 'HornyFurryDownloader-HFD/0.1'}

def parseUrl(url):
    parseUrl = urlparse(url).__getattribute__('path')[1:].split('/')[1]
    return parseUrl


def getData(postID):
    body = requests.get(f"https://e621.net/posts.json?tags=id:{postID}", headers=head)
    p = body.json()
    fileUrl = p['posts'][0]['file']['url']
    artistArray = p['posts'][0]['tags']['artist']
    artistName = ''
    if (len(artistArray) > 1):
        for a in artistArray:
            artistName = artistName + f'{a}, '
    else:
        artistName = artistArray = p['posts'][0]['tags']['artist'][0]

    data = [fileUrl, artistName]
    return data

def download(url, id, artist):
    file_ext = pathlib.Path(url).suffix
    fileRequest = requests.get(url, headers=head)

    if (os.path.exists(os.getcwd()+f'./output/{artist} - {id}{file_ext}') == True):
        print(f'file - {artist} - {id}{file_ext} already exists!')
        return 0
    else: 
        with open(f'./output/{artist} - {id}{file_ext}', 'wb') as f:
            total_length = int(fileRequest.headers.get('content-length'))
            for chunk in progress.bar(fileRequest.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()

def readFile(file):
    urls = file.read().split(',')
    return urls