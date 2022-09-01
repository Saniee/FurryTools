import os, requests, pathlib
from clint.textui import progress

name = input('Enter the Username of whom you will download theyere favs: ')

head = {'User-Agent': 'favDownloader/0.1'}

url = f'https://e621.net/posts.json?tags=fav:{name}'

if (os.path.isdir(os.getcwd()+"/output") != True):
    os.mkdir(os.getcwd()+f"/output")

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

    file_ext = pathlib.Path(fileUrl ).suffix
    fileRequest = requests.get(fileUrl, headers=head)

    if (len(artistArray) > 1):
        for a in artistArray:
            artistName = artistName + f'{a}, '
    else:
        artistName = artistArray = posts['posts'][i]['tags']['artist'][0]

    if (os.path.exists(os.getcwd()+f'./output/{artistName} - {postID}{file_ext}') == True):
        print(f'file - {artistName} - {postID}{file_ext} already exists!')
    else: 
        print(f'Downloading {artistName} - {postID}{file_ext}!')
        with open(f'./output/{artistName} - {postID}{file_ext}', 'wb') as f:
            total_length = int(fileRequest.headers.get('content-length'))
            for chunk in progress.bar(fileRequest.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
    
    i = i + 1