# -*- coding: utf-8 -*-

import os
import argparse
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from keras.optimizers import SGD
from keras.utils import np_utils

from deep_learning import get_data, generator_data, save_trained_model
from deep_learning.cnn.networks import LeNet, Simple

configs = {'IMAGES_SIZE': (128, 128)} 

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
  help="path to input dataset")
ap.add_argument("-s", "--save", required=True,
  type=str,
  help="name of the new model")
ap.add_argument("-t", "--type", required=True,
  type=str,
  help="type of training (simple or lenet)")
args = vars(ap.parse_args())

(data, labels) = get_data(args["dataset"])

# get all the different labels name in order to display them while prediction
labels_name = np.array(list(set(labels)))

number_of_classes = len(labels_name)

# encode the labels, converting them from strings to integers
le = LabelEncoder()
labels = le.fit_transform(labels)
labels = np_utils.to_categorical(labels, number_of_classes)

# split the data into two in order to find the accuracy after the training
(train_data, test_data, train_labels, test_labels) = train_test_split(
  data, labels, test_size=0.25, random_state=42)

# initialize the optimizer and model
print("[INFO] compiling model...")
opt = SGD(lr=0.001)

if args['type'] == 'simple':
  model = Simple.build(width=configs['IMAGES_SIZE'][0], height=configs['IMAGES_SIZE'][1],
    classes=number_of_classes)

else if args['type'] == 'lenet':
  model = LeNet.build(width=configs['IMAGES_SIZE'][0], height=configs['IMAGES_SIZE'][1], depth=3,
    classes=number_of_classes)

else:
  print('Invalid type')
  return 

model.compile(loss="binary_crossentropy", optimizer=opt,
  metrics=["accuracy"])

print("[INFO] training...")
model.fit_generator(generator_data(train_data, train_labels, configs['IMAGES_SIZE']),
  samples_per_epoch = len(train_data),
  nb_epoch = 20)

# show the accuracy on the testing set
print("[INFO] evaluating...")
(loss, accuracy) = model.evaluate_generator(generator_data(test_data, test_labels, configs['IMAGES_SIZE']),
  val_samples=len(test_data))
print("[INFO] accuracy: {:.2f}%".format(accuracy * 100))


print("[INFO} saving trained model...")
save_trained_model(args["save"], model, labels_name, configs)

print("[INFO] DONE")
