#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tensorflow as tf 
import numpy as np 
import crossData


batch_size = 8
# 36,32,3 -> 2560

h = 36
w = 32
input_channel = 3

# 导入数据
#trX, trY, teX, teY = input_MI_data.input_MI_data()
trX, trY, teX, teY = crossData.crossData()
print np.shape(trX),np.shape(trY),np.shape(teX),np.shape(teY)

#trX = trX - np.mean(trX)
#teX = teX - np.mean(teX)
#trX = (trX - np.min(trX)) / (np.max(trX) - np.min(trX))
#teX = (teX - np.min(teX)) / (np.max(teX) - np.min(teX))

trY = trY.T 
teY = teY.T
trX = trX.reshape(-1, h, w, input_channel)
teX = teX.reshape(-1, h, w, input_channel)

tr_Y = np.zeros((trY.shape[0], 2))
te_Y = np.zeros((teY.shape[0], 2))

#将target转化为2个输出处理
for i in xrange(trY.shape[0]):
    if trY[i][0] == 1.:
        tr_Y[i][0] = 1.
    else:
        tr_Y[i][1] = 1.

for i in xrange(teY.shape[0]):
    if teY[i][0] == 1.:
        te_Y[i][0] = 1.
    else:
        te_Y[i][1] = 1.

trY = tr_Y
teY = te_Y


#初始化权重
def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev = 0.01))
#建立模型
def model(X, w_layer_1, w_layer_2, w_layer_3, w_layer_4, w_layer_5, p_keep_conv, p_keep_hidden):
    '''
    参数解释：
    tf.nn.conv2d(X, w, strides = [1, 1, 1, 1], padding = 'SAME')
    X 表示从上一层输入的数据
    w 表示一个卷积核，比如一个3*3的高斯核
    strides 中的四个参数，第一个是 the number of images，第二个是 the hight of images，第三个是 the width of images，第四个是 the number of channels
    padding 表示图像周围是否需要填充，如果选择'SAME'参数，表示图像的输入和输出维度是一样的，那么在卷积的时候，模型就会在图像的周围填充上0。
            如果选择的是'VALID'参数，那么图像维度将会被改变，具体改变多少，视具体数据而定。
    tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = 'SAME')
    ksize 中的四个参数和strides中的参数一样
    '''
    l1a = tf.nn.relu(tf.nn.conv2d(X, w_layer_1, strides = [1, 1, 1, 1], padding = 'SAME'))
    l1 = tf.nn.max_pool(l1a, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = 'SAME')
    l1 = tf.nn.dropout(l1, p_keep_conv)

    l2a = tf.nn.relu(tf.nn.conv2d(l1, w_layer_2, strides = [1, 1, 1, 1], padding = 'SAME'))
    l2 = tf.nn.max_pool(l2a, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = 'SAME')
    l2 = tf.nn.dropout(l2, p_keep_conv)

    l3a = tf.nn.relu(tf.nn.conv2d(l2, w_layer_3, strides = [1, 1, 1, 1], padding = 'SAME'))
    l3 = tf.nn.max_pool(l3a, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = 'SAME')
    l3 = tf.reshape(l3, [-1, w_layer_4.get_shape().as_list()[0]])
    l3 = tf.nn.dropout(l3, p_keep_conv)

    l4 = tf.nn.relu(tf.matmul(l3, w_layer_4))
    l4 = tf.nn.dropout(l4, p_keep_hidden)

    pyx = tf.matmul(l4, w_layer_5)
    return pyx


# None表示batch的尺寸，第一个28表示图片的高度，第二个28表示图片的宽度，1表示channel的数量
X = tf.placeholder("float", [None, h, w, input_channel])
Y = tf.placeholder("float", [None, 2])

# 定义第一个卷积层 w_layer_1，其中3*3表示卷积核的尺寸，1表示channel的数量，32表示输出的通道数量
w_layer_1 = init_weights([3, 3, input_channel, 32])
# 定义第二个卷积层 w_layer_1，其中3*3表示卷积核的尺寸，32表示channel的数量，这个channel数量必须和上一层的输出通道相同，64表示输出的通道数量
w_layer_2 = init_weights([3, 3, 32, 64])
# 定义第三个卷积层 w_layer_1，其中3*3表示卷积核的尺寸，64表示channel的数量，这个channel数量必须和上一层的输出通道相同，128表示输出的通道数量
w_layer_3 = init_weights([3, 3, 64, 128])
# 定义第三个卷积层与下一层之间的全连接权重矩阵
w_layer_4 = init_weights([2560, 625])
# 定义全连接权重矩阵
w_layer_5 = init_weights([625, 2])


# dropout系数
p_keep_conv = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")

py_x = model(X, w_layer_1, w_layer_2, w_layer_3, w_layer_4, w_layer_5, p_keep_conv, p_keep_hidden)
print '---------', tf.shape(py_x), tf.shape(Y)
# 训练模型
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=py_x, labels=Y)) + tf.nn.l2_loss(w_layer_4) + tf.nn.l2_loss(w_layer_5)
# cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y)) + tf.nn.l2_loss(w_layer_4) + tf.nn.l2_loss(w_layer_5)
train_op = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cost)
predict_op = tf.argmax(py_x, 1)


with tf.Session() as sess:

    init = tf.initialize_all_variables()
    sess.run(init)
    ans = 0.0;index = 0;i=0
    while True:
        i+=1
        training_batch = zip(range(0, len(trX), batch_size), range(batch_size, len(trX), batch_size))
        #print training_batch
        print '----'
        for start, end in training_batch:
            #print start, end
            sess.run(train_op, feed_dict = {X: trX[start:end], Y: trY[start:end], 
                                            p_keep_conv: 0.8, p_keep_hidden: 0.5})

        tmp, cost_str = sess.run([predict_op, cost], feed_dict = {X: trX,
                                                          Y: trY,
                                                          p_keep_conv: 0.8,
                                                          p_keep_hidden: 0.5})

        print 'train: ', i, np.mean(np.argmax(teY, axis = 1) == tmp)
        print 'lost: ', cost_str
        tmp = np.mean(np.argmax(teY, axis = 1) ==
                        sess.run(predict_op, feed_dict = {X: teX,
                                                          Y: teY,
                                                          p_keep_conv: 1.0,
                                                          p_keep_hidden: 1.0}))

        print 'test: ', i, tmp
        #ans = max(ans, tmp)
        if tmp > ans:
            ans = tmp
            index = i
        print 'max test acc: ', ans, ', the index is: ', index


