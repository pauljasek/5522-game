# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 15:50:27 2019

@author: Paul Jasek
"""
#!pip install tensorflow-gpu==2.0.0-alpha0
import tensorflow as tf

from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model

class DQN(tf.keras.Model):
  def __init__(self, actions):
    super(DQN, self).__init__()
    self.conv1 = Conv2D(32, 3, activation='relu')
    self.flatten = Flatten()
    self.d1 = Dense(128, activation='relu')
    self.d2 = Dense(actions, activation='softmax')

  def call(self, x):
    x = self.conv1(x)
    x = self.flatten(x)
    x = self.d1(x)
    return self.d2(x)

dqn = DQN(3)

with tf.GradientTape() as tape:
  logits = dqn(images)
  loss_value = loss(logits, labels)

grads = tape.gradient(loss_value, model.trainable_variables)
optimizer.apply_gradients(zip(grads, model.trainable_variables))
