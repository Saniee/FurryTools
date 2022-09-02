from concurrent.futures import thread
import os
from tkinter import filedialog
import threading

import funcs

i = input('Enter Url or type in `file` here: ')


if (os.path.isdir(os.getcwd()+"/download") != True):
    os.mkdir(os.getcwd()+f"/download")

if (i == "file"):
    file = filedialog.askopenfile(initialdir=os.getcwd())
    urls = funcs.readFile(file)
    print(f'Downloading {len(urls)} posts!')
    for u in urls:
        postID = funcs.parseUrl(u)
        data = funcs.getData(postID)
        threading.Thread(target = funcs.download, args=(data[0], postID, data[1])).start()
else:
    postID = funcs.parseUrl(i)
    data = funcs.getData(postID)
    funcs.download(data[0], postID , data[1])