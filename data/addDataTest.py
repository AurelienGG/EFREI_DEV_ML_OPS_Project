import os
import unittest
from datetime import datetime
from addData import get_last_zip, add_new_data

class TestAddData(unittest.TestCase):
    def setUp(self):
        # Root folder 
        root_folder = os.path.dirname(__file__)

        # Define the root directory for test data
        self.root_dir = os.path.join(root_folder, "data")

        # Define the test data directory
        self.test_dir = os.path.join(root_folder, "test_data")

        # Create a destination directory for the test results
        self.destination_dir = os.path.join(root_folder, "test_results")

    def test_get_last_zip(self):
        # Call the get_last_zip function
        last_zip = get_last_zip(os.path.join(self.test_dir, "oldData_test"))

        # Assert that the last zip file is correct
        self.assertEqual(last_zip, "dataset_old_test_2024_02_27.zip")

    def test_add_new_data(self):
        datasets_dir = os.path.join(self.test_dir, "oldData_test")
        new_data_dir = os.path.join(self.test_dir, "newData_test")

        # Call the add_new_data function with the test directories
        add_new_data(datasets_dir, new_data_dir, self.destination_dir)

        # Generate the expected zip file name
        now = datetime.now()
        current_time = now.strftime("%Y_%m_%d_%Hh%M")
        expected_zip_name = f"dataset_{current_time}.zip"
        expected_zip_path = os.path.join(self.destination_dir, expected_zip_name)

        # Assert that the new zip file is created in the destination directory
        self.assertTrue(os.path.exists(expected_zip_path))

    def tearDown(self):
        # Clean up (if necessary)
        pass

if __name__ == "__main__":
    unittest.main()
