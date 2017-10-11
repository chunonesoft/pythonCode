#coding=utf-8
import socket

# host = "localhost"
#
# port = 10000
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# s.bind((host, port))
#
# s.listen(5)
#
# while 1:
#     sock, addr = s.accept()
#     print "got connection form ", sock.getpeername()
#     data = sock.recv(1024)
#     if not data:
#         break
#     else:
#         print data
import numpy as np
'''
配置参数
'''
#端口号
port = 8888
#ip地址
ipadress = 'localhost'
#Biosemi的通道数目
Channels = 64
#采样率
Samples = 16
'''
配置参数
'''
'''
变量
'''
#显示的通道数
DispChannel = 64
words = Channels * Samples
run = True
loop = 1000
t = 0
data_struct = np.zeros(Samples*loop, Channels)
data_struct2 = np.zeros(Samples, Channels)
'''
变量
'''
'''
打开tcp连接
'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ipadress, port)
s.listen(5)
s.recv(words*9)

while run:
    for L in range(0, loop - 1, 1):
        rawData = s.recv(3*words)
        np.reshape(rawData, (3, words))
        count = 3*words
        #将记录的tcp流中字节转化为32位无单位字符
        normaldata = rawData[2, :]*(256 ^ 3) + rawData[1, :]*(256 ^ 2) + rawData[0, :]*256 + 0
        #记录channels放进数组
        j = range(1 + (L * Samples), Samples+(L*Samples))
        i = range(0, words - 1, Channels)
        for d in range(Channels):
            data_struct[j, d] = int(normaldata[i+d])
            data_struct2[0:Samples, d] = int(normaldata[i+d])


s.close()
