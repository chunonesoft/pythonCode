import tensorflow as tf

hello = tf.constant('Hello, TensorFlow!')

a = tf.constant(10)
b = tf.constant(32)
sess = tf.Session()
print(sess.run(a+b))
# pynlpir.open()
# s = 'NLPIR分词系统前身为2000年发布的ICTCLAS词法分析系统，从2009年开始，为了和以前工作进行大的区隔，并推广NLPIR自然语言处理与信息检索共享平台，调整命名为NLPIR分词系统。'
#
# print (pynlpir.segment(s))
#
# print (pynlpir.get_key_words(s, weighted=False))

