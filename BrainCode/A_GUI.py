# coding=utf-8

import Tkinter as tk
from Tkinter import Menu    # 导入菜单类
from Tkinter    import *
import tkMessageBox
import threading
import csv

'''
连接Emotiv
'''
import ctypes
import sys
import os
from ctypes import *
from numpy import *
import time
from ctypes.util import find_library

try:
    print ctypes.util.find_library('edk.dll')
    print os.path.exists('.\\edk.dll')
    libEDK = cdll.LoadLibrary(".\\edk.dll")
except Exception,ex:
    print Exception, ":", ex

ED_COUNTER = 0
ED_INTERPOLATED=1
ED_RAW_CQ=2
ED_AF3=3
ED_F7=4
ED_F3=5
ED_FC5=6
ED_T7=7
ED_P7=8
ED_O1=9
ED_O2=10
ED_P8=11
ED_T8=12
ED_FC6=13
ED_F4=14
ED_F8=15
ED_AF4=16
ED_GYROX=17
ED_GYROY=18
ED_TIMESTAMP=19
ED_ES_TIMESTAMP=20
ED_FUNC_ID=21
ED_FUNC_VALUE=22
ED_MARKER=23
ED_SYNC_SIGNAL=24
#         IN DLL(edk.dll)
#         typedef enum EE_DataChannels_enum {
#            ED_COUNTER = 0, ED_INTERPOLATED, ED_RAW_CQ,
#            ED_AF3, ED_F7, ED_F3, ED_FC5, ED_T7,
#            ED_P7, ED_O1, ED_O2, ED_P8, ED_T8,
#            ED_FC6, ED_F4, ED_F8, ED_AF4, ED_GYROX,
#            ED_GYROY, ED_TIMESTAMP, ED_ES_TIMESTAMP, ED_FUNC_ID, ED_FUNC_VALUE, ED_MARKER,
#            ED_SYNC_SIGNAL
#         } EE_DataChannel_t;

targetChannelList = [ED_COUNTER,ED_AF3, ED_F7, ED_F3, ED_FC5, ED_T7,ED_P7, ED_O1, ED_O2, ED_P8, ED_T8,ED_FC6, ED_F4, ED_F8, ED_AF4, ED_GYROX, ED_GYROY, ED_TIMESTAMP, ED_FUNC_ID, ED_FUNC_VALUE, ED_MARKER, ED_SYNC_SIGNAL]
header = ['COUNTER','AF3','F7','F3', 'FC5', 'T7', 'P7', 'O1', 'O2','P8', 'T8', 'FC6', 'F4','F8', 'AF4','GYROX', 'GYROY', 'TIMESTAMP','FUNC_ID', 'FUNC_VALUE', 'MARKER', 'SYNC_SIGNAL']
write = sys.stdout.write
try:
    eEvent      = libEDK.EE_EmoEngineEventCreate()
    eState      = libEDK.EE_EmoStateCreate()
except Exception,ex:
    print 'libEDK'

userID            = c_uint(0)
nSamples   = c_uint(0)
nSam       = c_uint(0)
nSamplesTaken  = pointer(nSamples)
da = zeros(128,double)
data     = pointer(c_double(0))
user                    = pointer(userID)
composerPort          = c_uint(1726)
secs      = c_float(1)
datarate    = c_uint(0)
readytocollect    = False
option      = c_int(0)
state     = c_int(0)



win = tk.Tk()
win.title("脑电运动想象系统")    # 添加标题

# 获取屏幕的大小
screenwidth = win.winfo_screenwidth()
screenheight = win.winfo_screenheight() - 100


bm1 = PhotoImage(file='rest.gif')
bm2 = PhotoImage(file='ready.gif')
bm3 = PhotoImage(file='left.gif')
bm4 = PhotoImage(file='right.gif')

label = Label(win, image=bm1,anchor = "center")
label2 = Label(win,text="1")
label.bm = bm1

def changeImage(i):
    t1 = threading.Thread(target=testThread)
    print threading.Event()
    if i % 3 == 1:
        label.configure(image = bm1)
        i = i + 1
        label.after(2000,changeImage,i)
    elif i % 3 == 2:
        label.configure(image=bm2)
        i = i + 1
        label.after(1000, changeImage,i)
    else:
        t1.setDaemon(True)
        t1.start()
        label.configure(image=bm3)
        i = i + 1
        label.after(6000, changeImage, i)
def testThread():
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
# 对应 "开始实验" 按钮
def _startTest():
    i = 1
    label.pack(fill=X, expand=1)
    i = i + 1

    label.after(2000, changeImage, i)
    win.update_idletasks()
    win.deiconify()  # now window size was calculated
    #win.withdraw()  # hide window again

def _saveData():
    print "Start receiving EEG Data! Press any key to stop logging...\n"
    # f = file('EEG.csv', 'w')
    f = open('EEG.csv', 'w')
    print >> f, header
    hData = libEDK.EE_DataCreate()
    libEDK.EE_DataSetBufferSizeInSec(secs)
    print "Buffer size in secs:"
    while (1):
        state = libEDK.EE_EngineGetNextEvent(eEvent)
        if state == 0:
            eventType = libEDK.EE_EmoEngineEventGetType(eEvent)
            libEDK.EE_EmoEngineEventGetUserId(eEvent, user)
            if eventType == 16:  # libEDK.EE_Event_enum.EE_UserAdded:
                print "User added"
                libEDK.EE_DataAcquisitionEnable(userID, True)
                readytocollect = True

        if readytocollect == True:
            libEDK.EE_DataUpdateHandle(0, hData)
            libEDK.EE_DataGetNumberOfSample(hData, nSamplesTaken)
            print "Updated :", nSamplesTaken[0]
            if nSamplesTaken[0] != 0:
                nSam = nSamplesTaken[0]
                arr = (ctypes.c_double * nSamplesTaken[0])()
                ctypes.cast(arr, ctypes.POINTER(ctypes.c_double))
                # libEDK.EE_DataGet(hData, 3,byref(arr), nSam)
                data = array('d')  # zeros(nSamplesTaken[0],double)
                for sampleIdx in range(nSamplesTaken[0]):
                    for i in range(22):
                        libEDK.EE_DataGet(hData, targetChannelList[i], byref(arr), nSam)
                        print >> f, arr[sampleIdx], ",",
                    print >> f, '\n'
        time.sleep(0.2)
    libEDK.EE_DataFree(hData)

# 对应 "退出系统" 按钮
def _quit():
    """结束主事件循环"""
    win.quit()      # 关闭窗口
    win.destroy()   # 将所有的窗口小部件进行销毁，应该有内存回收的意思
    exit()
# 对应 "连接emotiv" 按钮
def _connectEmotiv():
    try:
        if libEDK.EE_EngineRemoteConnect("127.0.0.1", composerPort) != 0:
            print "Cannot connect to EmoComposer on"
            tkMessageBox.showinfo(title='连接Emotiv', message="连接Emotiv失败")
        tkMessageBox.showinfo(title='连接Emotiv', message="连接Emotiv成功")
    except Exception,ex:
        print Exception, ":", ex
        tkMessageBox.showinfo(title='连接Emotiv', message="连接Emotiv失败")


def _disconnectEmotiv():
    try:
        libEDK.EE_EngineDisconnect()
        tkMessageBox.showinfo(title='关闭Emotiv', message="关闭Emotiv成功")
    except Exception,ex:
        print Exception, ":", ex
        tkMessageBox.showinfo(title='关闭Emotiv', message="关闭Emotiv失败")

def _about():
    tkMessageBox.showinfo(title='关于我们', message="本系统由浙江工业大学HCI实验室开发")
    readExcel()

def readExcel():
    data = csv.reader(open("EEG.csv"),encoding='utf-8')
    return data


# 创建菜单栏功能
menuBar = Menu(win)
win.config(menu=menuBar)

# 创建一个名为 "操作" 的菜单项
fileMenu = Menu(menuBar)
menuBar.add_cascade(label="操作", menu=fileMenu)

# 在菜单项 "操作" 下面添加一个名为 "设置采集信息" 的选项
fileMenu.add_command(label="设置采集信息")

# 添加一条横线
fileMenu.add_separator()

# 在菜单项 "操作" 下面添加一个名为 "连接Emotiv" 的选项
fileMenu.add_command(label="连接Emotiv", command=_connectEmotiv)

# 在菜单项 "操作" 下面添加一个名为 "关闭Emotiv" 的选项
fileMenu.add_command(label="关闭Emotiv", command=_disconnectEmotiv)

# 添加一条横线
fileMenu.add_separator()

# 在菜单项 "操作" 下面添加一个名为 "开始实验" 的选项
fileMenu.add_command(label="开始实验", command=_startTest)

# 添加一条横线
fileMenu.add_separator()

# 在菜单项 "操作" 下面添加一个名为 "退出系统" 的选项
fileMenu.add_command(label="退出系统", command=_quit)

# 添加一条横线
fileMenu.add_separator()

algorithmMenu = Menu(menuBar)
menuBar.add_cascade(label="分析算法", menu=algorithmMenu)
algorithmMenu.add_radiobutton(label="CNN")
# 添加一条横线
algorithmMenu.add_separator()
algorithmMenu.add_radiobutton(label="CSP+SVM")
# 添加一条横线
algorithmMenu.add_separator()
algorithmMenu.add_radiobutton(label="CSP+BP")
# 添加一条横线
algorithmMenu.add_separator()
algorithmMenu.add_radiobutton(label="WPT1+SVM")
# 添加一条横线
algorithmMenu.add_separator()
algorithmMenu.add_radiobutton(label="WPT2+SVM")
# 添加一条横线
algorithmMenu.add_separator()
algorithmMenu.add_radiobutton(label="WPT1+SVM")
# 添加一条横线
algorithmMenu.add_separator()
algorithmMenu.add_radiobutton(label="Mu")


# 创建一个名为File的菜单项
helpMenu = Menu(menuBar)

# 在菜单栏中创建一个名为Help的菜单项helpMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="关于", menu=helpMenu)
# 在菜单栏Help下添加一个名为About的选项
helpMenu.add_command(label="关于系统", command=_about)


win.resizable(False, False)

win.geometry('%sx%s+%s+%s' % (screenwidth, screenheight, 0,0))


win.mainloop()      # 当调用mainloop()时,窗口才会显示出来
