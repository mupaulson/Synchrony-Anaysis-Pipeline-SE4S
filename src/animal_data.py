"""
This script is a command-line utility for processing animal data.
It leverages the AnimalData class to load data from a specified CSV file,
perform operations on the data, and then save the processed data to another
CSV file. The script accepts input and output file names as command-line
arguments.

Usage:
    python load_data.py -i [input_filename] -o [output_filename]

Where:
    -i: Specifies the input CSV file path.
    -o: Specifies the output CSV file path.

The script includes:
    - A function to parse command-line arguments.
    - A main function to handle the data loading and saving operations.
"""

import csv
import sys


class AnimalData:
    """
    A class to represent animal data extracted from CSV files.

    Attributes:
        animal_num (int): A unique identifier for the animal,
                          extracted from the CSV filename.
        cell_data (dict): A dictionary where keys are cell names
                          and values are lists of (timestamp,
                          elapsed_time, value) tuples.

    Methods:
        get_data_for_cell(cell, n=None): Returns a list of (timestamp,
                                         value) tuples for the specified cell.
        get_data_at_time(timestamp):     Returns a dictionary with cells as
                                         keys and measurements at a specific
                                         timestamp as values.
        save_to_csv(output_path):        Saves the cell data into a CSV file
                                         at the specified path.
        from_csv(filepath):              Class method to create an AnimalData
                                         instance from a CSV file.
    """
    def __init__(self, animal_num, cell_data):
        """
        Initializes the AnimalData object with animal number and cell data.

        Parameters:
            animal_num (int): A unique identifier for the animal.
            cell_data (dict): Cell data as a dictionary where keys are cell
                              names and values are lists of (timestamp,
                              elapsed_time, value) tuples.
        """
        # Extracted from the CSV filename
        self.animal_num = animal_num
        # Dictionary where keys are cell names, and values are lists
        # of (timestamp, elapsed_time, value) tuples
        self.cell_data = cell_data

    def get_data_for_cell(self, cell, n=None):
        """
        Return a list of (timestamp, value) tuples for the specified cell.

        Parameters:
            cell (str): The name of the cell to retrieve data for.
                        n (int, optional): Number of data points to return.
                        If None, returns all data for the cell.

        Returns:
            list: A list of (timestamp, value) tuples for the specified cell.
        """
        data = self.cell_data.get(cell, [])
        return data[:n] if n else data

    def get_data_at_time(self, timestamp):
        """
        Return a dictionary where keys are cells and values are measurements
        at the specified timestamp.

        Parameters:
            timestamp (float): The specific timestamp to retrieve data for.

        Returns:
            dict: A dictionary with cells as keys and their corresponding
                  measurements at the given timestamp as values.
        """
        result = {}
        for cell, values in self.cell_data.items():
            matching_data = None
            for t, v in values:
                if t == timestamp:
                    matching_data = (t, v)
                    break
            if matching_data is None:
                matching_data = (None, None)
            result[cell] = matching_data
        return result

    def save_to_csv(self, output_path):
        """
        Save the cell data to a CSV file.

        Parameters:
            output_path (str): Path to save the output CSV file.
        """
        # Extract headers
        cells = list(self.cell_data.keys())
        headers = ['Unnamed: 0', 'time', 'elapsed'] + cells  # Updated headers

        # Prepare rows
        rows = []
        # Extract timestamp and elapsed_time
        for i, cell_data_tuple in enumerate(self.cell_data[cells[0]]):
            timestamp, elapsed_time, _ = cell_data_tuple
            # Start with index, timestamp, and elapsed time
            row = [i, timestamp, elapsed_time]
            for cell in cells:
                # Add cell values (third element in tuple)
                row.append(self.cell_data[cell][i][2])
            rows.append(row)

        # Write to CSV
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write header
            writer.writerows(rows)  # Write data rows

    @classmethod
    def from_csv(cls, filepath):
        """
        Class method to create an AnimalData instance from a CSV file.

        Parameters:
            filepath (str): Path to the CSV file to be read.

        Returns:
            AnimalData: An instance of the AnimalData class initialized
                        with data from the CSV file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If there is an error converting animal num to an int.
            Exception: For other errors encountered while reading the file.
        """
        try:
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Read the header row
                header = [cell.strip() for cell in header]
                start_cell_columns = header[3:]
                # Cell data starts from the 4th column
                cell_data = {cell: [] for cell in start_cell_columns}

                for row in reader:
                    # Timestamp is the second column
                    timestamp = float(row[1])
                    # Elapsed time is the third column
                    elapsed_time = float(row[2])
                    values = row[3:]  # Extracting cell data values
                    for cell, value in zip(start_cell_columns, values):
                        cell_tuple = (timestamp, elapsed_time, float(value))
                        cell_data[cell].append(cell_tuple)

        except FileNotFoundError:
            sys.stderr.write("File not found\n")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading from file: {e}")
            sys.exit(1)
        # Extract animal number from filename
        filename = filepath.split("/")[-1]
        animal_num_str = filename[:4]

        try:
            animal_num = int(animal_num_str)
        except ValueError as e:
            print(f"Error converting animal number to integer: {e}")

        return cls(animal_num, cell_data)
