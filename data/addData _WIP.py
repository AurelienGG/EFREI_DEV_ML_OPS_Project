import os
import shutil
import zipfile
from datetime import datetime
from PIL import Image
import numpy as np

# Function to retrieve the last zip file in a directory
def get_last_zip(directory):
    zip_files = [file for file in os.listdir(directory) if file.endswith('.zip')]
    if zip_files:
        return zip_files[-1]
    else:
        return None

# Function to copy folder content to another location
def copy_folder_content(src, dest):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks=False, ignore=None)
        else:
            shutil.copy2(s, d)

# Function to compare two images
def compare_images(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    image1_array = np.array(image1)
    image2_array = np.array(image2)
    return np.array_equal(image1_array, image2_array)

# Function to add images to binData or tmpNewData
def add_images(src_folder, dest_folder, bin_folder):
    new_images = 0
    bin_images = 0
    for item in os.listdir(src_folder):
        if os.path.isdir(os.path.join(src_folder, item)):
            if os.path.exists(os.path.join(dest_folder, item)):
                for image in os.listdir(os.path.join(src_folder, item)):
                    src_image_path = os.path.join(src_folder, item, image)
                    dest_image_path = os.path.join(dest_folder, item, image)
                    if not os.path.exists(dest_image_path) or not compare_images(src_image_path, dest_image_path):
                        shutil.copy2(src_image_path, dest_image_path)
                        new_images += 1
                    else:
                        shutil.copy2(src_image_path, os.path.join(bin_folder, item))
                        bin_images += 1
            else:
                copy_folder_content(os.path.join(src_folder, item), os.path.join(dest_folder, item))
                new_images += len(os.listdir(os.path.join(src_folder, item)))
    return new_images, bin_images

# Main function
def main():
    root_folder = os.path.dirname(__file__)
    datasets_dir = os.path.join(root_folder, "datasets")
    new_data_dir = os.path.join(root_folder, "newData")
    bin_data_dir = os.path.join(root_folder, "binData")
    add_data_dir = os.path.join(root_folder, "tmpNewData")

    # Retrieve the last .zip file in datasets
    last_zip = get_last_zip(datasets_dir)
    if not last_zip:
        print("No zip file found in datasets directory.")
        return

    # Retrieve the dataset.zip file in newData
    new_data_zip = os.path.join(new_data_dir, "dataset.zip")
    if not os.path.exists(new_data_zip):
        print("dataset.zip not found in newData directory.")
        return

    # Create a folder called tmpNewData
    if not os.path.exists(add_data_dir):
        os.makedirs(add_data_dir)

    # Unzip both zip files locally
    with zipfile.ZipFile(os.path.join(datasets_dir, last_zip), 'r') as datasets_zip:
        datasets_zip.extractall(add_data_dir)

    with zipfile.ZipFile(new_data_zip, 'r') as new_data_zip:
        new_data_zip.extractall(add_data_dir)

    # Add images to binData or tmpNewData
    new_images, bin_images = add_images(os.path.join(new_data_dir, "dataset"), add_data_dir, bin_data_dir)

    # Count the number of images in newData
    num_new_data_images = sum(len(files) for _, _, files in os.walk(os.path.join(new_data_dir, "dataset")))

    print("Number of images in newData:", num_new_data_images)
    print("Number of images added:", new_images)
    print("Number of images in binData:", bin_images)

    # Zip the folders of tmpNewData
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%Hh%M")
    new_zip_name = f"dataset_{current_time}.zip"
    shutil.make_archive(os.path.join(root_folder, new_zip_name), 'zip', add_data_dir)

if __name__ == "__main__":
    main()