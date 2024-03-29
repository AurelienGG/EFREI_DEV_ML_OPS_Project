# Imports
import cv2
import numpy as np
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import datetime
from tensorflow import keras
from tensorflow.keras.models import Model
import tensorflow as tf
import os
import pathlib
import requests
import zipfile
import math

"""## Les réseaux de neurones convolutionnels CNN"""

# GitHub repository URL
repo_url = "https://api.github.com/repos/AurelienGG/EFREI_DEV_ML_OPS_Project/contents/data/datasets"

# Send a GET request to GitHub API
response = requests.get(repo_url)

if response.status_code == 200:
    # Extract file information from the response JSON
    files_info = response.json()

    # Filter out directories and get only file names
    files = [file_info['name'] for file_info in files_info if file_info['type'] == 'file']

    # Filter out non-zip files
    zip_files = [f for f in files if f.endswith('.zip')]

    if zip_files:
        # Construct the URL of the most recent zip file
        most_recent_file_name = max(zip_files)

        # Construct the URL of the most recent zip file
        most_recent_file_url = f"https://github.com/AurelienGG/EFREI_DEV_ML_OPS_Project/raw/Clement/data/datasets/{most_recent_file_name}"

        # Download the most recent zip file
        response = requests.get(most_recent_file_url)

        if response.status_code == 200:
            # Write the content of the zip file to disk
            with open('dataset.zip', 'wb') as f:
                f.write(response.content)

            try:
                # Extract the downloaded zip file
                with zipfile.ZipFile('dataset.zip', 'r') as zip_ref:
                    zip_ref.extractall('/content/datasets')

                # Set the data directory to the extracted folder
                data_dir = pathlib.Path('/content/datasets/dataset')
                print(data_dir)
                print(os.path.abspath(data_dir))
            except zipfile.BadZipFile:
                print("Error: The downloaded file is not a valid zip file.")
        else:
            print("Failed to download the most recent zip file.")
    else:
        print("No .zip files found in the repository.")
else:
    print("Failed to fetch repository contents from GitHub.")

# Function to count the number of image files in a directory
def count_images(directory):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    image_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_count += 1
    return image_count

# Assuming data_dir is the directory where the zip file is extracted
data_dir = '/content/datasets/dataset'

# Count the number of images
num_images = count_images(data_dir)

print("Number of images:", num_images)

img_height = 200
img_width = 200

# Assuming num_images is already calculated from the previous step

# Calculate a reasonable batch size
optimal_batch_size = math.ceil(num_images / 10)  # You can adjust the denominator as needed

# Limit the batch size to a maximum value if needed
max_batch_size = 32  # You can adjust this value as needed
optimal_batch_size = min(optimal_batch_size, max_batch_size)

# Set the batch size
batch_size = optimal_batch_size

# Use the calculated batch size in image_dataset_from_directory function
train_data = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=(img_height, img_width),
    batch_size=batch_size,
)

val_data = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(img_height, img_width),
    batch_size=batch_size,
)

class_names = val_data.class_names
print("Class Names:", class_names)
print("Batch Size:", batch_size)

# Count the number of subdirectories (classes)
num_classes = len([name for name in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, name))])

# Use the count of subdirectories as the number of classes
num_classes = num_classes if num_classes > 0 else 1  # Ensure at least one class

# Use the calculated number of classes in image_dataset_from_directory function
train_data = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    class_names=None,  # Automatically infer class names from subdirectories
    shuffle=True,
)

val_data = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    class_names=None,  # Automatically infer class names from subdirectories
    shuffle=True,
)

print("Number of Classes:", num_classes)

from tensorflow.keras import layers

model = tf.keras.Sequential([
    layers.experimental.preprocessing.Rescaling(1./255),
    layers.Conv2D(128, 4, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 4, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 4, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(16, 4, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

logdir = "logs"

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=20
)

# Extract the best accuracy
best_accuracy = max(history.history['accuracy'])

print("Best Training Accuracy:", best_accuracy)

model.summary()

from datetime import datetime
import tensorflow as tf

# Assuming 'model' is your TensorFlow model
# Save the model
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
model_filename = f'model_{current_datetime}.h5'
model.save(model_filename)

# Create a report file
report_filename = f'report_{current_datetime}.txt'
with open(report_filename, 'w') as report_file:
    report_file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_file.write(f"Accuracy: {best_accuracy}\n")
    report_file.write("Dataset name: data_dir\n")  # Replace with the actual dataset name

print("Files created successfully:")
print(model_filename)
print(report_filename)

