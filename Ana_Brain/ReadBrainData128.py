#coding=utf-8

import scipy.io as scio
from compiler.ast import flatten
import numpy as np
from sklearn.model_selection import train_test_split

def input_MI_data(filename1,filename2,filename3,labelname):
    temp1 = np.ones((36, 1))
    temp2 = np.ones((24, 1))
    temp = np.ones((60, 1))


    data1 = scio.loadmat(filename1)['ss']
    data2 = scio.loadmat(filename2)['ss']
    data3 = scio.loadmat(filename3)['ss']
    label = scio.loadmat(labelname)['label']

    label = label - temp
    '''
    原始数据维度data1[20,30720]
    最终数据维度data[60,3channel*256Hz*6s]
    '''
    data = np.zeros((60, 4608), np.float32)
    #4608 = 64*72
    for i in range(20):
        data[i] = flatten(data1[:,i*128*6:(i+1)*128*6].tolist())
        data[i+20] = flatten(data2[:,i*128*6:(i+1)*128*6].tolist())
        data[i+40] = flatten(data3[:,i*128*6:(i+1)*128*6].tolist())
    x_train, x_test, y_train, y_test = train_test_split(data, label, test_size=0.4, random_state=0)
    print x_train.shape
    print x_test.shape
    print y_train.shape
    print y_test.shape
    print y_train
    return x_train,  np.transpose(y_train), x_test, np.transpose(y_test)


#input_MI_data('sxq1_Segmentation.dat.mat','sxq2_Segmentation.dat.mat','sxq3_Segmentation.dat.mat')