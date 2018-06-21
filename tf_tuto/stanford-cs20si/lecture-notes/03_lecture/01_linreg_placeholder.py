import os
import time
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

os.environ['TP_CPP_MIN_LOG_LEVEL'] = '2'

import utils

DATA_FILE = '../data/birth_life_2010.txt'

# Step 1: read in data
data, n_samples = utils.read_birth_life_data(DATA_FILE)

# Step 2: create placeholders for X (birth_rate) and Y (life expectancy)
X = tf.placeholder(tf.float32, name='X')
Y = tf.placeholder(tf.float32, name='Y')

# Step 3: create weight and bias, initialize to 0
w = tf.get_variable('weights', initializer=tf.constant(0.0))
b = tf.get_variable('bias', initializer=tf.constant(0.0))

# Step 4: build the model to predict Y
Y_predicted = w * X + b

# Step 5: use the squared error as the loss function
# Mean squared error
MSE_loss = tf.square(Y - Y_predicted, name='loss')
# Huber error
Hubre_loss = utils.huber_loss(Y, Y_predicted)

# Step 6: Use GD t minimize the loss
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001).minimize(MSE_loss)


start = time.time()
writer = tf.summary.FileWriter('./graphs/linear_reg', tf.get_default_graph())
with tf.Session() as sess:
    # Step 7: initialze the necessary variables, in this case W and b
    sess.run(tf.global_variables_initializer())

    # Step 8: Train the model for 100 epochs
    for i in range(100):
        total_loss = 0
        for x, y in data:
            # Session execute optimizer and fetch value of loss
            _, loss = sess.run([optimizer, MSE_loss], feed_dict={X: x, Y: y})
            total_loss += loss

        if i % 10 == 0:
            print('Epoch {0}: {1}'.format(i, total_loss/n_samples))

    # close the writer when done
    writer.close()

    # Step 9: output the value of W and b
    w_out, b_out = sess.run([w, b])

print('Took: %f seconds' % (time.time() - start))

# plot the results
plt.plot(data[:, 0], data[:, 1], 'bo', label='Real data')
plt.plot(data[:, 0], data[:, 0] * w_out + b_out, 'r', label='Predicted data')
plt.legend()
plt.show()