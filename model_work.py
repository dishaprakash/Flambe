from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras import regularizers
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, AveragePooling2D

inception = InceptionV3(weights='imagenet', include_top=False)
x = inception.output
x = GlobalAveragePooling2D()(x)
x = Dense(128,activation='relu')(x)
x = Dropout(0.2)(x)
predictions = Dense(10, kernel_regularizer=regularizers.l2(0.005), activation='softmax')(x)
model = Model(inputs=inception.input, outputs=predictions)
model.load_weights("best_model_10class.hdf5")
categories = [ 'pizza', 'cheesecake', 'chicken_wings', 'samosa', 'onion_rings', 'fish_and_chips','fried_rice', 'garlic_bread', 'waffles', 'hamburger']
categories.sort()


def predict_class(img_file):
    img = image.load_img(img_file, target_size=(299, 299))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.

    pred = model.predict(img)
    index = np.argmax(pred)
    categories.sort()
    pred_value = categories[index]
    return pred_value
