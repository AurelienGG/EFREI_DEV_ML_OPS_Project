import os
import shutil
import zipfile
from datetime import datetime

def get_last_zip(directory):
    zip_files = [file for file in os.listdir(directory) if file.endswith('.zip')]
    if zip_files:
        return max(zip_files)
    else:
        return None

def add_new_data(datasets_dir, new_data_dir, destination_dir=None):
    last_dataset_zip = get_last_zip(datasets_dir)
    if not last_dataset_zip:
        print("No existing dataset found.")
        return

    # Create tmpNewData folder if it doesn't exist
    tmp_new_data_dir = os.path.join(os.path.dirname(datasets_dir), "tmpNewData")
    if not os.path.exists(tmp_new_data_dir):
        os.makedirs(tmp_new_data_dir)

    # Unzip the last dataset
    with zipfile.ZipFile(os.path.join(datasets_dir, last_dataset_zip), 'r') as datasets_zip:
        datasets_zip.extractall(tmp_new_data_dir)

    # Unzip the new data
    new_data_zip_filename = get_last_zip(new_data_dir)
    new_data_zip = os.path.join(new_data_dir, new_data_zip_filename)
    if not os.path.exists(new_data_zip):
        print("dataset.zip not found in newData directory.")
        return

    with zipfile.ZipFile(new_data_zip, 'r') as new_data_zip:
        new_data_zip.extractall(tmp_new_data_dir)

    # Zip the updated dataset in destination_dir or tmpNewData folder
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%Hh%M")
    new_zip_name = f"dataset_{current_time}"
    if destination_dir:
        shutil.make_archive(os.path.join(destination_dir, new_zip_name), 'zip', tmp_new_data_dir)
    else:
        shutil.make_archive(os.path.join(datasets_dir, new_zip_name), 'zip', tmp_new_data_dir)

    print("New data added successfully.")

    # Remove the tmpNewData folder
    shutil.rmtree(tmp_new_data_dir)

def main():
    root_folder = os.path.dirname(__file__)
    datasets_dir = os.path.join(root_folder, "datasets")
    new_data_dir = os.path.join(root_folder, "newData")
    #destination_dir = os.path.join(root_folder, "test_results")  # Change this to the desired destination folder

    #add_new_data(datasets_dir, new_data_dir, destination_dir)
    add_new_data(datasets_dir, new_data_dir)

if __name__ == "__main__":
    main()
