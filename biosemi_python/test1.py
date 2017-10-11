#coding=utf-8
from Tkinter import *

colors = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')

root = Tk()
f = Frame(root, height=200, width=200)
f.color = 0
f['bg'] = colors[f.color]
def foo():
    f.color = (f.color+1)%(len(colors))
    f['bg'] = colors[f.color]
    f.after(500, foo)
f.pack()
f.after(500, foo)

mainloop()