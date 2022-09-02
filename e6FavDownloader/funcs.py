import pathlib,requests,os

def download(fileUrl, artistName, postID, head):
    file_ext = pathlib.Path(fileUrl).suffix
    fileRequest = requests.get(fileUrl, headers=head)

    if (os.path.exists(os.getcwd()+f'./download/{artistName} - {postID}{file_ext}') == True):
        print(f'File - {artistName} - {postID}{file_ext} already exists!')
    else:
        print(f'Downloading {artistName} - {postID}{file_ext}!')
        with open(f'./download/{artistName} - {postID}{file_ext}', 'wb') as f:
            f.write(fileRequest.content)