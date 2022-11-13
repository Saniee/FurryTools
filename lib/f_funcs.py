import pathlib
import requests
import os

from PIL import ImageTk, Image
from io import BytesIO


def download(fileUrl, artistName, postID, head, d, viewWindowImg):
    file_ext = pathlib.Path(fileUrl).suffix
    fileRequest = requests.get(fileUrl, headers=head)

    if (os.path.exists(d + f'{artistName} - {postID}{file_ext}') == True):
        print(f'File - {artistName} - {postID}{file_ext} already exists!')
    else:
        print(f'Downloaded {artistName} - {postID}{file_ext}!')
        with open(d + f'/{artistName} - {postID}{file_ext}', 'wb') as f:
            f.write(fileRequest.content)

    if (file_ext == ".jpg" or file_ext == ".png" or file_ext == ".gif"):
        img = ImageTk.PhotoImage(Image.open(
            BytesIO(fileRequest.content)).resize((750, 750), Image.ANTIALIAS))
        viewWindowImg.configure(image=img)
        viewWindowImg.image = img
