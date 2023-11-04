#!/usr/bin/env python3

import readline
import tensorflow as tf

@tf.keras.utils.register_keras_serializable(package='Custom', name=None)
def text_standardizer(input_data):
    lowercase = tf.strings.lower(input_data)
    return lowercase

with tf.keras.utils.CustomObjectScope({'text_standardizer': text_standardizer}):
    model = tf.keras.models.load_model('final_model')
    model.summary()

    while True:
        inp = [i.strip() for i in input('> ').split('.')]
        while "" in inp:
            inp.remove("")
        output = model.predict(inp)
        score = sum(output) / len(output)
        print(["UwU" if i > 0.5 else "Normal" for i in output])
        print("Final judgement:", "UwU" if score > 0.5 else "Normal")
