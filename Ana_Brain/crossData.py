#coding=utf-8
'''
Created on 2016年11月23日
@author: chunsoft
'''
import scipy.io as scio
from compiler.ast import flatten
import numpy as np

def crossData():
    temp = np.ones((140,1))
    data = scio.loadmat('dataset_BCIcomp1.mat')
    
    datatest = scio.loadmat('labels_data_set_iii.mat')
    Y_test = datatest['y_test']
    X_test = data['x_test']
    X_train = data['x_train']
    Y_train = data['y_train']
    #x_train = np.zeros((100,3456),np.float32)
    #x_test = np.zeros((40,3456),np.float32)
    x_train = np.zeros((140,3456),np.float32)
    x_test = np.zeros((140,3456),np.float32)
   
    for i in xrange(140):
        x_train[i] = flatten(X_train[:,:,i].tolist());  
        x_test[i] = flatten(X_test[:,:,i].tolist());
    y_train = Y_train - temp;
    y_test = Y_test - temp;
    #x_train,x_test,y_train,y_test = cross_validation.train_test_split(x_data,Y,test_size=0.3,random_state=0)   
    return x_train,np.transpose(y_train),x_test,np.transpose(y_test)
