import argparse
import os
import requests
import threading

import funcs

arg = argparse.ArgumentParser('favDownload')
arg.add_argument('name', help='The name of the user you want favorites from.')
arg.add_argument('-limit', required=False, default=75, help='The amount of favorites you want to download. The MAX is 320.')

args = arg.parse_args()

def main():
    name = args.name # input('Enter the Username of whom you will download theyere favs: ')
    limit = args.limit # input('Enter how much favorites you want to download (MAX is 320): ')

    if (int(limit) > 320):
        print('I am sorry but the hard limit is 320.')
        print('Running again...')
        main()

    url = f'https://e621.net/posts.json?tags=fav:{name}&limit={limit}'

    if (os.path.isdir(os.getcwd()+"/download") != True):
        os.mkdir(os.getcwd()+f"/download")

    head = {'User-Agent': 'favDownloader/0.1'}

    body = requests.get(url, headers=head)
    p = body.json()

    if (body.status_code == 403):
        print(f'The user {name} has blocked access to theyre favorites.')
        print('Running again...')
        main()

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
                artistName = artistName[:-1]
        else:
            artistName = artistArray = p['posts'][i]['tags']['artist'][0]

        threading.Thread(target=funcs.download, args=(
            fileUrl, artistName, postID, head)).start()

        i = i + 1

main()