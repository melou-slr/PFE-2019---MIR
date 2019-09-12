# -*- coding: utf-8 -*-
"""CNNSSM-cluster-downbeat.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qTnVx3s-Fk4SRj_ExBQHGu6vzwhusv6t
"""

import os
import os.path
from os import path
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from matplotlib import patches
import keras

from PIL import Image
import pylab as pyl

from keras import models
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import TensorBoard

import time

# Initialising the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(16, (8, 8), padding='same', input_shape = (50, 50, 3), activation = 'tanh'))
classifier.add(MaxPooling2D(pool_size=(6, 6)))
classifier.add(Conv2D(32, (6, 3), padding='same', activation = 'tanh'))

# Step 2 - Flattening
classifier.add(Flatten())

# Step 3 - Full connection
classifier.add(Dropout(0.5))
classifier.add(Dense(units = 128, activation = 'tanh'))
classifier.add(Dropout(0.5)) 
classifier.add(Dense(units = 1, activation = 'sigmoid'))

classifier.summary()

#Compiling the CNN
from keras.optimizers import Adamax

classifier.compile(loss='binary_crossentropy',optimizer=Adamax(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0),metrics=['acc'])

base_dir = '/workdir/soler/SSMs_with_metergram/'
train_dir = '/workdir/soler/SSMs_with_metergram/Train/'
validation_dir = '/workdir/soler/SSMs_with_metergram/Validation/'



# Directory with our training SMJ_nonsolo pictures
train_SMJ_nonsolo_dir = '/workdir/soler/SSMs_with_metergram/Train/Non_segment'

# Directory with our training SMJ_solo pictures
train_SMJ_solo_dir = '/workdir/soler/SSMs_with_metergram/Train/Segment'


# Directory with our test SMJ_nonsolo pictures
validation_SMJ_nonsolo_dir = os.path.join(validation_dir, 'Non_segment')

# Directory with our test SMJ_solo pictures
validation_SMJ_solo_dir = os.path.join(validation_dir, 'Segment')

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# All images will be rescaled by 1./255
train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)



# Flow training images in batches of 128 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
        directory=train_dir,  # This is the source directory for training images
        target_size=(50, 50),  # All images will be resized to 100*100
        batch_size=128,
        # Since we use binary_crossentropy loss, we need binary labels
        class_mode='binary')

# Flow validation images in batches of 128 using validation_datagen generator
validation_generator = validation_datagen.flow_from_directory(
        directory=validation_dir,
        target_size=(50, 50),
        batch_size=128,
        class_mode='binary')

# checkpoint
filepath="/workdir/soler/SSMdownbeatsyncwith-weights-improvement-{epoch:02d}-{val_acc:.2f}.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

history = classifier.fit_generator(
      train_generator,
      steps_per_epoch=270,  # nb images = batch_size * steps
      epochs=25,
      validation_data=validation_generator,
      validation_steps=25,  # nb images = batch_size * steps
      verbose=1,
      class_weight = { 0 : 1, 1 : 3},
      callbacks=callbacks_list)

classifier.save('/workdir/soler/my_model_test_architecture article_onlySSMdownbeatwith_25epochs_tansigmoid_weight3.h5')