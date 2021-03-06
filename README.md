# Deep learning env

Coded in Python, with OpenCV & TensorFlow & Keras, this project follows machine 
learning & deep learning concepts to able computer vision.

Software by Benjamin HAOUI & Kevin DIDELOT.

## Prerequisites

- [Vagrant](https://www.vagrantup.com)
	
	Plugins: vagrant-vbguest

- [Ansible](http://docs.ansible.com/ansible)

See [Help install](https://github.com/zirkis/LILO/blob/master/docs/installation.md)

## Install
	
```bash
cd <path_to_project>/vagrant
vagrant up --provision
```

Can take up to an hour and a half (depends on your connection and your computer)

## Connect

```bash
vagrant ssh
```

## Collect data

First thing we have to activate the workspace env.

```bash
WORKSPACE
```

Now we have to create a folder to store all the data that we want to add in 
the future in the dataset.

```bash
mkdir data_on_preparation
```

Now we have to collect as much data as possible, they are multiple way to do it.

<p align="center">
  <img src="https://github.com/zirkis/LILO/blob/master/docs/images/prepare_data.jpeg"
  alt="multiple way to collect data"/>
</p>

### Manually

If you already have some data just create a subdirectory in `data_on_preparation` for
each label and copy paste all your data in it.

<b>Note</b>: Check for each subdirectories that all the data correspond to the good label.

The expected result:

	data_on_preparation/
		|
		|__ plane/
		|	|__ plane_1.jpg
		|	|__ plane_2.jpg
		|	....
		|	|__ plane_n.jpg
		|__car/
		|	|__ car_1.jpg
		|	|__ car_2.jpg
		|	....
		|	|__ car_n.jpg
		|_house/
			|__ house_1.jpg
			|__ house_2.jpg
			....
			|__ house_n.jpg

The name of the images doesn't matter

Formats accepted:
- jpg
- png
- bmp

### From video

You can extract the frame from the video in order to get more data.

Just create a new script:

```bash
touch extract_frame_from_video.py
```

Then copy paste the following code, then change the path to your video, the label and 
the frequency to extract the frame (frequency=2 => One image in two will be taken) 

```python
# -*- coding: utf-8 -*-
from deep_learning import extract_frame_from_video

if __name__ == '__main__':
  
  path_to_save = 'data_on_preparation'
  path_to_video = "path/to/your/video"
  frequency = 2
  label = 'your_label'

  extract_frame_from_video(path_to_videos,
    	frequency, '{}/{}'.format(path_to_save, label))
    
```

<b>Note</b>: Take a frequency too low is not a good idea because the difference between the 
previous image will be very low, this will cause an over-training of your label.

Then execute the script:


```bash
python extract_frame_from_video.py
```

### From web

## Sort all collected data

At the moment you should have a folder with one or more subdirectories(label) containing many images.

Before insert this data in the dataset, you have to check that all the images match with the appropriate label.
Indeed data in the wrong label can cause a dataset degradation.

<p align="center">
  <img src="https://github.com/zirkis/LILO/blob/master/docs/images/sort_data_before_insert.jpeg"
  alt="sort data before insert"/>
</p>

## Insert data in dataset

<p align="center">
  <img src="https://github.com/zirkis/LILO/blob/master/docs/images/insert_in_dataset.jpeg"
  alt="insert data in dataset"/>
</p>

Now that all your collected data are "clean", you can now add them in your dataset 
without taking risk to corrupt it.

So create a new script: 

```bash
touch insert_in_dataset.py
```

Copy paste the following code, then change the label, the path to add (matching your label), 
and the path to your dataset.

```python
# -*- coding: utf-8 -*-
from deep_learning import insert_in_dataset

if __name__ == '__main__':
	label = 'your_label'
	path_to_add = 'path/to/label'
	path_dataset = 'path/to/dataset'

	insert_in_dataset(label, path_to_add, path_dataset) 
```

<b>Note</b>: All your images will be converted to jpg, and a need name will be given (uuid).
If some images are not convertable to jpg, they will not be taken in the dataset.

## Training 

This step is the more technical one, we will have to choice a way to train the model.
Fortunately your package contains several ways to train a cnn (Convolutional Neural Networks).
But before we can train our model with our dataset we have to do some works.

### Include all we need for the futur

```python
# -*- coding: utf-8 -*-

import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from keras.optimizers import SGD
from keras.utils import np_utils

from deep_learning import get_data, generator_data, save_trained_model
from deep_learning.cnn.networks import Simple
```

### Set all the configs for the training

```python
configs = {'IMAGES_SIZE': (64, 64)} 
```

### Retrieving data

```python
path_to_dataset="path/to/your/dataset"

(data, labels) = get_data(path_to_dataset)
```

The function get_data return:

- data: An array containning all the path to the data in the given dataset
- labels: A cross array with the data array containning the label of the cross data 

### Prepare data

```python
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
```

### Compile model

```python
opt = SGD(lr=0.001)

model = Simple.build(width=configs['IMAGES_SIZE'][0], height=configs['IMAGES_SIZE'][1],
	classes=number_of_classes)


model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])
```

### Training

```python
model.fit_generator(generator_data(train_data, train_labels, configs['IMAGES_SIZE']),
	samples_per_epoch = len(train_data),
	nb_epoch = 20)
```

### Evaluate

```python
(loss, accuracy) = model.evaluate_generator(generator_data(test_data, test_labels, configs['IMAGES_SIZE']),
	val_samples=len(test_data))
print("[INFO] accuracy: {:.2f}%".format(accuracy * 100))
```

### Save trained model

```python
path_to_save = path/where/you/want/to/save
save_trained_model(path_to_save, model, labels_name, configs)
```

## Predict a label

At the moment we are now able to predict a label on one given image

### Include all we need

```python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
from keras.models import model_from_json
```

### Load image

```python
path_to_image = path/to/the/image/to/predict
image = cv2.imread(path_to_image)
```

### Load the trained model

```python
path_to_model = path/to/the/trained/model
(model, labels, configs) = load_saved_trained_model(path_to_model)
```

### Prepare image for prediction

```python
image = np.array(cv2.resize(image, configs['IMAGES_SIZE'])) / 255.0
image = np.expand_dims(image.transpose((2,0,1)), axis=0)
```

### Prediction

```python
classes = model.predict(image)
```

### See result 

```python
np.set_printoptions(formatter={'float_kind':'{:f}'.format})
print("RESULT:")
for i in range(0, len(classes[0])):
	print("{}: {}".format(labels[i], classes[0][i] * 100))
```

## More examples

[Examples](https://github.com/zirkis/LILO/blob/master/app/deep_learning/examples)
