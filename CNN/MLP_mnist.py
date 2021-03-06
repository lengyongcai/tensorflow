#coding:utf-8
""" 
Created on 2016-07-15 @author: yongcai
使用多层感知机训练MNIST数据集，同时使用Dropout, Adagrad, ReLU
"""


from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf

mnist = input_data.read_data_sets("./MNIST_data/", one_hot=True)

sess = tf.InteractiveSession()


in_units = 784
h1_units = 300

W1 = tf.Variable(tf.truncated_normal([in_units, h1_units], stddev=0.1))
b1 = tf.Variable(tf.zeros([h1_units]))
W2 = tf.Variable(tf.zeros([h1_units, 10]))
b2 = tf.Variable(tf.zeros([10]))

x = tf.placeholder(tf.float32, [None, in_units])
keep_prob = tf.placeholder(tf.float32)
y_ = tf.placeholder(tf.float32, [None, 10])

hidden1 = tf.nn.relu(tf.matmul(x, W1) + b1)
hidden1_drop = tf.nn.dropout(hidden1, keep_prob)

y = tf.nn.softmax(tf.matmul(hidden1_drop, W2) + b2)

cross_entropy = tf.reduce_sum(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

train_step = tf.train.AdadeltaOptimizer(0.3).minimize(cross_entropy)

init = tf.initialize_all_variables()

sess.run(init)

for i in range(3000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    train_step.run({x: batch_xs, y_: batch_ys, keep_prob: 0.75})


correct_prection = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_sum(tf.cast(correct_prection, tf.float32))

print(accuracy.eval({x: batch_xs, y_: batch_ys, keep_prob: 1.0}))



