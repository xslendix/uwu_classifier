#!/usr/bin/env python3

import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf

from tensorflow.keras.saving import register_keras_serializable
from tensorflow.keras import layers
from tensorflow.keras import losses

print(tf.__version__)

BATCH_SIZE = 32
SEED = 69420

print('Loading training dataset')
raw_train_ds = tf.keras.utils.text_dataset_from_directory(
    'dataset',
    batch_size=BATCH_SIZE,
    subset='training',
    seed=SEED,
    label_mode="int",
    class_names=['normal', 'uwu'],
    validation_split=0.2,
)

print('Loading validation dataset')
raw_val_ds = tf.keras.utils.text_dataset_from_directory(
    'dataset',
    batch_size=BATCH_SIZE,
    subset='validation',
    seed=SEED,
    label_mode="int",
    class_names=['normal', 'uwu'],
    validation_split=0.2,
)

print('Loading testing dataset')
raw_test_ds = tf.keras.utils.text_dataset_from_directory(
    'dataset',
    batch_size=BATCH_SIZE,
    label_mode="int",
    class_names=['normal', 'uwu'],
)

@tf.keras.utils.register_keras_serializable(package='Custom', name=None)
def text_standardizer(input_data):
    lowercase = tf.strings.lower(input_data)
    return lowercase

MAX_FEATURES = 10000
SEQUENCE_LENGTH = 240

vectorize_layer = layers.TextVectorization(
        standardize=text_standardizer,
        max_tokens=MAX_FEATURES,
        output_mode='int',
        output_sequence_length=SEQUENCE_LENGTH
        )

train_text = raw_train_ds.map(lambda x, y: x)
vectorize_layer.adapt(train_text)

def vectorize_text(text, label):
    text = tf.expand_dims(text, -1)
    return vectorize_layer(text), label

#text_batch, label_batch = next(iter(raw_train_ds))
#first_message, first_label = text_batch[0], label_batch[0]
#print('Message', first_message)
#print('Label', first_label)
#print('Vectorized message', vectorize_text(first_message, first_label))

train_ds = raw_train_ds.map(vectorize_text)
val_ds = raw_val_ds.map(vectorize_text)
test_ds = raw_test_ds.map(vectorize_text)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

print('Creating model')

EMBEDDING_DIM = 16

model = tf.keras.Sequential([
  layers.Embedding(MAX_FEATURES, EMBEDDING_DIM),
  layers.Dropout(0.2),
  layers.GlobalAveragePooling1D(),
  layers.Dropout(0.2),
  layers.Dense(1)])

model.summary()

model.compile(loss=losses.BinaryCrossentropy(from_logits=True),
              optimizer='adam',
              metrics=tf.metrics.BinaryAccuracy(threshold=0.0))

epochs = 10
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs)

loss, accuracy = model.evaluate(test_ds)

print("Loss: ", loss)
print("Accuracy: ", accuracy)

history_dict = history.history
history_dict.keys()

acc = history_dict['binary_accuracy']
val_acc = history_dict['val_binary_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)

print('Exporting model')

export_model = tf.keras.Sequential([
  vectorize_layer,
  model,
  layers.Activation('sigmoid')
])

export_model.compile(
    loss=losses.BinaryCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
)

# Test it with `raw_test_ds`, which yields raw strings
loss, accuracy = export_model.evaluate(raw_test_ds)
print(accuracy)

print('Saving model')
export_model.save('final_model', save_format='tf')

while True:
    export_model.predict([input('> ')])
