#coding=utf-8
import tensorflow as tf
'''
('v1:', array([[ 0.64324552,  1.30941129]], dtype=float32))
('v2:', array([[-0.56216162, -1.40646005]], dtype=float32))
'''
# 使用和保存模型代码中一样的方式来声明变量
v1 = tf.Variable(tf.random_normal([1, 2]), name="v1")
v2 = tf.Variable(tf.random_normal([1, 2]), name="v2")
saver = tf.train.Saver()
with tf.Session() as sess:
    saver.restore(sess, "Model/test_model.ckpt")
    print("v1:", sess.run(v1))
    print("v2:", sess.run(v2))
    print("Model Restored")