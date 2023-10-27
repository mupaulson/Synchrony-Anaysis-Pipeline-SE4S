import unittest
import os
import sys

sys.path.insert(0, '../../src')  # noqa
from load_data import adjust_timestamps, THRESHOLD

sys.path.insert(0, '../../src')  # noqa
from animal_data import AnimalData

class TestLoadData(unittest.TestCase):

    def setUp(self):
        """Setup mock data for testing."""
        self.animal1 = AnimalData.from_csv("../../data/4659-test2.csv")
        self.animal2 = AnimalData.from_csv("../../data/4807-test2.csv")

        self.animal1.remap_time_values()
        self.animal2.remap_time_values()

    def test_adjust_timestamps(self):
        """Test the adjust_timestamps function."""
        adjust_timestamps(self.animal1, self.animal2)
        
        # Check if timestamps are adjusted
        for i in range(len(self.animal1.cell_data["C000"])):
            timestamp1 = self.animal1.cell_data["C000"][i][0]
            timestamp2 = self.animal2.cell_data["C000"][i][0]
            
            # Ensure the difference between timestamps is within threshold
            self.assertTrue(abs(timestamp1 - timestamp2) <= THRESHOLD)

    def test_adjust_timestamps_no_change(self):
        """Test that adjust_timestamps doesn't change timestamps if difference is greater than the threshold."""
        mock_data3 = AnimalData(["C000", "C001"], {"C000": [(0.0, 1), (0.2501, 2), (0.5002, 3)], "C001": [(0.0, 1), (0.2501, 2), (0.5002, 3)]})
        mock_data4 = AnimalData(["C000", "C001"], {"C000": [(0.0, 1), (0.2, 2), (0.4, 3)], "C001": [(0.0, 1), (0.2, 2), (0.4, 3)]})

        adjust_timestamps(mock_data3, mock_data4)
        
        # Check that timestamps weren't adjusted because the difference exceeds the threshold
        self.assertNotEqual(mock_data3.cell_data["C000"][1][0], mock_data4.cell_data["C000"][1][0])
        
    def test_invalid_data_handling(self):
        """Test that the function raises an error for mismatched datasets."""
        mock_data5 = AnimalData(["C000"], {"C000": [(0.0, 1), (0.2, 2)]})
        mock_data6 = AnimalData(["C000"], {"C000": [(0.0, 1), (0.2, 2), (0.4, 3)]})

        with self.assertRaises(ValueError):
            adjust_timestamps(mock_data5, mock_data6)

    def tearDown(self):
        """Clean up after tests."""
        # If your tests create files or modify any shared resources, clean them up here.
        if os.path.exists("../data/4659-test2-remap.csv"):
            os.remove("../data/4659-test2-remap.csv")
        if os.path.exists("../data/4807-test2-remap.csv"):
            os.remove("../data/4807-test2-remap.csv")

if __name__ == "__main__":
    unittest.main()
