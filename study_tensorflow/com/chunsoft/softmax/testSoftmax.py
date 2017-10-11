#coding=utf-8

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

sess = tf.InteractiveSession()
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32, [None, 784])

W = tf.Variable(tf.zeros([784, 10]))

b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x, W) + b)

y_ = tf.placeholder(tf.float32, [None, 10])

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y), reduction_indices=[1]))

#梯度下降优化器,学习效率为0.5，优化目标为cross_entropy
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

#全局参数初始化器
tf.global_variables_initializer().run()

for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    train_step.run({x: batch_xs, y_: batch_ys})
# tf.argmax是从一个tensor中寻找最大值的符号，
# tf.argmax(y,1)求各个预测数据概率最大的那一个
# tf.equal判断预测的数据类别是否就是正确的类别
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
#tf.cast将之前correct_prediction输出的bool值转换为float32，再求平均
accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

print(accuracy.eval({x: mnist.test.images, y_: mnist.test.labels}))




