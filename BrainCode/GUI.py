#coding=utf-8
from Tkinter import *
from connectBiosemi import ActiveTwo
#导入tk模块
top = Tk()
#初始化Tk
top.title('运动想象脑电实验')
# 初始化
#device = ActiveTwo(host='127.0.0.1', sfreq=512, port=778, nchannels=32, tcpsamples=4)
#top.withdraw()  # hide window
# 获取屏幕的宽度和高度，并且在高度上考虑到底部的任务栏，为了是弹出的窗口在屏幕中间
screenwidth = top.winfo_screenwidth()
screenheight = top.winfo_screenheight() - 100
top.resizable(False, False)
# #标题显示为label test
# label = Label(top, text = 'this is my first label')
# #创建一个label，它属于top窗口，文本显示内容为.....
# label.pack()
# bm = PhotoImage(file = 'left.gif')
# label2 = Label(top, image = bm)
# label2.bm = bm
# label2.pack()
# top.mainloop()
# #进入消息循环
bm1 = PhotoImage(file='rest.gif')
bm2 = PhotoImage(file='ready.gif')
bm3 = PhotoImage(file='left.gif')
bm4 = PhotoImage(file='right.gif')

label = Label(top, image=bm1,anchor = "center")
label.bm = bm1
i = 1
f = open('label.txt','a')

def changeImage(i):
    if i % 3 == 1:
        label.configure(image = bm1)
        i = i + 1
        label.after(2000,changeImage,i)
    elif i % 3 == 2:
        label.configure(image = bm2)
        i = i + 1
        label.after(1000, changeImage,i)
    else:
        label.configure(image = bm3)
        f.write('1')
        f.write('\n')
        i = i + 1
        label.after(6000, changeImage, i)

        # #读取2s数据
        # for run in range(2):
        #     rawdata = device.read(duration=1.0)
        #     print rawdata

label.pack(fill=X,expand=1)
i = i + 1
label.after(2000,changeImage,i)
top.update_idletasks()
top.deiconify()    #now window size was calculated
top.withdraw()     #hide window again
# top.geometry('%sx%s+%s+%s' % (top.winfo_width() + 10, top.winfo_height() + 10, (screenwidth - top.winfo_width())/2,
#  (screenheight - top.winfo_height())/2) )    #center window on desktop
top.geometry('%sx%s+%s+%s' % (screenwidth, screenheight, 0,0))
# top.geometry('%sx%s+%s+%s' % (300 + 10, 300 + 10, (screenwidth - 300)/2,
#  (screenheight - 300)/2))    #center window on desktop
top.deiconify()
top.mainloop()