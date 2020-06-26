from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D, Input, Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam, RMSprop
from keras_preprocessing.image import ImageDataGenerator
from DataProcessing.util import NUM_TYPES
import pandas as pd
import numpy as np
import pdb
import os
import pathlib


INPUT_SHAPE = (96, 96, 3)
IMAGE_SIZE = (96, 96)
KERNAL_SIZE = [(11,11), (3,3)]
FILTERS = [4, 8, 16, 32, 64, 128]
BATCH_SIZE_TRAIN = 1
BATCH_SIZE_TEST = 1


# Simple sequential model for quick testing
def build_simple_model():

    model = Sequential()
    model.add(Conv2D(filters=16, kernel_size=(11,11), input_shape=(96,96,3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Flatten())
    model.add(Dense(17, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics='accuracy')
    model.summary()

    return model


# Duplicated CNN 
def build_model():
    pass
