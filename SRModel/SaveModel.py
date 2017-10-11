#coding=utf-8
'''
('v1:', array([[ 0.64324552,  1.30941129]], dtype=float32))
('v2:', array([[-0.56216162, -1.40646005]], dtype=float32))
'''
# 模型获取，然后保存
import tensorflow as tf
v1=tf.Variable(tf.random_normal([1, 2]), name="v1")
v2=tf.Variable(tf.random_normal([1, 2]), name="v2")

init_op=tf.global_variables_initializer()
saver=tf.train.Saver()

with tf.Session() as sess:
    sess.run(init_op)
    print("v1:", sess.run(v1)) # 打印v1、v2的值一会读取之后对比
    print("v2:", sess.run(v2))
    # 判断统一
    # 定义保存路径，一定要是绝对路径，且用‘/ ’分隔父目录与子目录
    saver_path = saver.save(sess, "Model/test_model.ckpt")
    print("Model saved in file:", saver_path)