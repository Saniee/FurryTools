import os
from tkinter import filedialog

import funcs

i = input('Enter Url or type in `file` here: ')


if (os.path.isdir(os.getcwd()+"/output") != True):
    os.mkdir(os.getcwd()+f"/output")

if (i == "file"):
    file = filedialog.askopenfile(initialdir=os.getcwd())
    urls = funcs.readFile(file)
    for u in urls:
        postID = funcs.parseUrl(u)
        data = funcs.getData(postID)
        funcs.download(data[0], postID, data[1])
else:
    postID = funcs.parseUrl(i)
    data = funcs.getData(postID)
    funcs.download(data[0], postID , data[1])
