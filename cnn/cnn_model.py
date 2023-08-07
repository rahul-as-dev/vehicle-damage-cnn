import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import tensorflow as tf
from keras.applications import DenseNet169
from keras.models import Model, load_model
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from keras.layers import Dense
import pathlib

# Damage class = [broken-head-or-tail-lamp, side-dents, front-dents, back-dents, glass-shatter, scratches, no-damage]

# CNN -> VGG16, DenseNET169 -> 10 layers (freeze the layers except last one) + apply a dense layer classification layer.
# IMAGENET (1.2 million across 1000 categories)

"""
Classes related to car in imagenet :
estate car
car mirror
car wheel
passenger car
race car, racing car
sports car, sport car
streetcar
"""
"""
Transfer learning : The intuition is that some knowledge is specific to individual domains,
while some knowledge may be common between different domains which may help to improve
performance for the target domain / task.

However, in the cases where the source domain and target domain are not related to each other,
brute-force transfer may be unsuccessful and can lead to the degraded performance. In our case,
we use the CNN models which are trained on the Imagenet dataset. Since the Imagenet dataset contains car as a class,
we expect the transfer to be useful which we extensively validate by experimenting with multiple pre-trained models.
"""
# use transfer learning by utilizing pretrained model (DenseNet-169) and

base_dir = "cnn";
train_data_directory = base_dir + "/data/training";
validation_data_directory = base_dir + "/data/validation";

damage_class = os.listdir(train_data_directory)
img_width, img_height, channel = 224, 224, 3
batch_size = 20

# Define data augmentation generator
train_data_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    fill_mode='nearest'
)

# Define your data generators
train_generator = train_data_gen.flow_from_directory(
    train_data_directory,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'
)

# Define data generator for validation and test data
valid_data_gen = ImageDataGenerator(rescale=1./255)
# test_data_gen = ImageDataGenerator(rescale=1./255)

valid_generator = valid_data_gen.flow_from_directory(
    validation_data_directory,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# test_generator = test_data_gen.flow_from_directory(
#     'validation_data_directory',
#     target_size=(224, 224),
#     batch_size=32,
#     class_mode='categorical'
# )
class_names = train_generator.classes
batch_images, batch_labels = train_generator.next()
# Configure the plot settings
plt.figure(figsize=(25, 25))
plt.subplots_adjust(hspace=0.5)
# Plot the images
# for i in range(len(batch_images)):
#     plt.subplot(4, 8, i+1)
#     plt.imshow(batch_images[i])
# #     plt.title("Class: {}".format(batch_labels[i]))
#     plt.axis('off')
#
# # Show the plot
# plt.show()


pretrained_model = DenseNet169(weights='imagenet', include_top=False, input_shape=(img_width, img_height, channel))


# Freeze the pre-trained layers
for layer in pretrained_model.layers:
    layer.trainable = False

"""
# Freeze the pre-trained layers
for layer in pretrained_model.layers[:-4]:
    layer.trainable = False
"""

# Modify the last fully connected layer for our custom classes
num_classes = 7  # Number of damage classes + "no damage"
x = pretrained_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)

# Define the custom CNN model
custom_model = Model(inputs=pretrained_model.input, outputs=predictions)

# Compile the model
custom_model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model with validation data
num_epochs = 10  # Adjust as needed
history = custom_model.fit(
    train_generator,
    epochs=num_epochs,
    validation_data=valid_generator
)

# Evaluate the model on the test data
# test_loss, test_accuracy = custom_model.evaluate(test_generator)
# print(f"Test Loss: {test_loss:.4f}")
# print(f"Test Accuracy: {test_accuracy:.4f}")

# Save the trained model
custom_model.save('inspection_model.keras')

# Load the trained model
model = load_model('inspection_model.keras')
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


target_size = (img_width, img_height)

# Load and preprocess the new image
img_path = "/Users/rahul_jha/Downloads/predict-img1.jpeg"  # Replace with the path to your new image
img = image.load_img(img_path, target_size=target_size)
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
img = img / 255.0  # Normalize the image data

# Make predictions
predictions = custom_model.predict(img)
print(predictions)

def predictDamageScore(image_path):
    img = image.load_img(image_path, target_size=(224, 224))  # Assuming target size is 224x224
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize the image

    predictions = custom_model.predict(img_array)
    predicted_class = np.argmax(predictions[0])  # Get the index of the predicted class

    return predicted_class
