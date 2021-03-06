# -*- coding: utf-8 -*-
"""faace recognization

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dt1jfs7fNcCw-jr8qH0GSjILc0O0ClOM
"""

from keras.applications import VGG16

model = VGG16(weights = 'imagenet', 
                 include_top = False, 
                 input_shape = (224, 224, 3))

for layer in model.layers:
    layer.trainable = False

def addTopModel(bottom_model, num_classes, D=256):
    """creates the top or head of the model that will be 
    placed ontop of the bottom layers"""
    top_model = bottom_model.output
    top_model = Flatten(name = "flatten")(top_model)
    top_model = Dense(D, activation = "relu")(top_model)
    top_model = Dropout(0.3)(top_model)
    top_model = Dense(num_classes, activation = "softmax")(top_model)
    return top_model

model.input

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.models import Model

num_classes = 2

FC_Head = addTopModel(model, num_classes)

modelnew = Model(inputs=model.input, outputs=FC_Head)

print(modelnew.summary())

from keras.preprocessing.image import ImageDataGenerator

train_data_dir = "/content/drive/My Drive/Colab Notebooks/data/train"
validation_data_dir = "/content/drive/My Drive/Colab Notebooks/data/test"

train_datagen = ImageDataGenerator(
      rescale=1./255,
      rotation_range=20,
      width_shift_range=0.2,
      height_shift_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest')
 
validation_datagen = ImageDataGenerator(rescale=1./255)
 
# Change the batchsize according to your system RAM
train_batchsize = 16
val_batchsize = 10
 
train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(224, 224),
        batch_size=train_batchsize,
        class_mode=('categorical'))
validation_generator = validation_datagen.flow_from_directory(
                validation_data_dir,
                target_size=(224, 224),
                batch_size=val_batchsize,
                class_mode='categorical',
                shuffle = False,)

from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint, EarlyStopping
                   
checkpoint = ModelCheckpoint("gk_detection.h5",
                             monitor="val_loss",
                             mode="min",
                             save_best_only = True,
                             verbose=1)

earlystop = EarlyStopping(monitor = 'val_loss', 
                          min_delta = 0, 
                          patience = 3,
                          verbose = 1,
                          restore_best_weights = True)

# we put our call backs into a callback list
callbacks = [earlystop, checkpoint]

# Note we use a very small learning rate 
modelnew.compile(loss = 'categorical_crossentropy',
              optimizer = RMSprop(lr = 0.001),
              metrics = ['accuracy'])

nb_train_samples = 300
nb_validation_samples = 40
epochs = 5
batch_size = 3

history = modelnew.fit_generator(
    train_generator,
    steps_per_epoch = nb_train_samples // batch_size,
    epochs = epochs,
    callbacks = callbacks,
    validation_data = validation_generator,
    validation_steps = nb_validation_samples // batch_size)

modelnew.save("gk_detection.h5")

from keras.models import load_model
import cv2
import numpy as np

model = load_model('/content/gk_detection.h5')

input_im = cv2.imread('/content/2018-11-04-13-28-55-938.jpg')
input_im = cv2.resize(input_im, (224, 224), interpolation = cv2.INTER_LINEAR)
input_im = input_im / 255.
input_im = input_im.reshape(1,224,224,3)

res = np.argmax(model.predict(input_im, 1, verbose = 0), axis=1)

if res == 1:
  print("gourav")
else:
  print("dst")

train_generator.class_indices

