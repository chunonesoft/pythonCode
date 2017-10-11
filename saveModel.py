#coding=utf-8
import tensorflow as tf
import numpy as np
import os

#输入数据
x_data = np.linspace(-1,1,300)[:, np.newaxis]
noise = np.random.normal(0,0.05, x_data.shape)
y_data = np.square(x_data)-0.5+noise

#输入层
xs = tf.placeholder(tf.float32, [None, 1])
ys = tf.placeholder(tf.float32, [None, 1])

#隐层
W1 = tf.Variable(tf.random_normal([1,10]))
b1 = tf.Variable(tf.zeros([1,10])+0.1)
Wx_plus_b1 = tf.matmul(xs,W1) + b1
output1 = tf.nn.relu(Wx_plus_b1)

#输出层
W2 = tf.Variable(tf.random_normal([10,1]))
b2 = tf.Variable(tf.zeros([1,1])+0.1)
Wx_plus_b2 = tf.matmul(output1,W2) + b2
output2 = Wx_plus_b2

#损失
loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-output2),reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

#模型保存加载工具
saver = tf.train.Saver()

#判断模型保存路径是否存在，不存在就创建
if not os.path.exists('tmp/'):
    os.mkdir('tmp/')

#初始化
sess = tf.Session()
if os.path.exists('tmp/checkpoint'): #判断模型是否存在
    saver.restore(sess, 'tmp/model.ckpt') #存在就从模型中恢复变量
else:
    init = tf.global_variables_initializer() #不存在就初始化变量
    sess.run(init)

#训练
for i in range(1000):
    _,loss_value = sess.run([train_step,loss], feed_dict={xs:x_data,ys:y_data})
    if(i%50==0): #每50次保存一次模型
        save_path = saver.save(sess, 'tmp/model.ckpt') #保存模型到tmp/model.ckpt，注意一定要有一层文件夹，否则保存不成功！！！
        print("模型保存：%s 当前训练损失：%s"%(save_path, loss_value))