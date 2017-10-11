#coding=utf-8
from Tkinter import *
import Tkinter as tk
import time

root = Tk()

# root.geometry("400x400")
# entry = Entry(root)
#
# w = tk.Label(root,
#              height = 20,
#              width = 20,
#              #padx = 10,
#              #pady = 20,
#              #background="blue",
#              #borderwidth=10,
#              #relief = "ridge",
#              text="运动想象脑电实验",
#              justify = "right",
#              foreground = "red",
#              anchor = "center"
#              )
# w.pack()
w = Canvas(
           root,
           width=200,
           height=200,
           background="white"
          )
w.pack()

yellowLine = w.create_line(0,100,200,100,fill='yellow')
root.mainloop()
time.sleep(5)

w.delete(yellowLine)





# root.geometry("400x400")
# entry = Entry(root)
#
# button = Button(root, text='search')
# listbox = Listbox(root, bg='white')
# photo = PhotoImage(file='right.gif')
# label = Label(image=photo)
# entry.grid(row=0, column=0)
# button.grid(row=0, column=1)
# listbox.grid(row=1, column=0, columnspan=2, sticky=W+E)
# label.grid(row=2, column=0)
