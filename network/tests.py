import tensorflow as tf
import time
import numpy as np

# Simple matrix multiplication to see if CPU is used
a = tf.random.normal((10000, 10000))
b = tf.random.normal((10000, 10000))

start = time.time()
c = tf.matmul(a, b)
tf.print("Result shape:", tf.shape(c))
tf.print("Elapsed seconds:", time.time() - start)
