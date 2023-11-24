import csv
import sys

class AnimalData:
    def __init__(self, animal_num, cell_data):
        self.animal_num = animal_num  # Extracted from the CSV filename
        self.cell_data = cell_data  # Dictionary where keys are cell names, and values are lists of (timestamp, value) tuples

    def get_data_for_cell(self, cell, n=None):
        """Return a list of (timestamp, value) tuples for the specified cell."""
        data = self.cell_data.get(cell, [])
        return data[:n] if n else data

    def get_data_at_time(self, timestamp):
        """Return a dictionary where keys are cells and values are measurements at the specified timestamp."""
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
        """Save the cell data to a CSV file."""
        # Extract headers
        cells = list(self.cell_data.keys())
        headers = ['Unnamed: 0', 'time', 'elapsed'] + cells  # Updated headers

        # Prepare rows
        rows = []
        for i, (timestamp, elapsed_time, _) in enumerate(self.cell_data[cells[0]]):  # Extracting timestamp and elapsed_time
            row = [i, timestamp, elapsed_time]  # Start with index, timestamp, and elapsed time
            for cell in cells:
                row.append(self.cell_data[cell][i][2])  # Add cell values (third element in tuple)
            rows.append(row)

        # Write to CSV
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write header
            writer.writerows(rows)  # Write data rows

    @classmethod
    def from_csv(cls, filepath):
        """Class method to create an AnimalData instance from a CSV file."""
        try:
            with open(filepath, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Read the header row
                header = [cell.strip() for cell in header]
                start_cell_columns = header[3:]

                cell_data = {cell: [] for cell in start_cell_columns} # Cell data starts from the 4th column

                for row in reader:
                    timestamp = float(row[1])  # Timestamp is the second column
                    elapsed_time = float(row[2])  # Elapsed time is the third column
                    values = row[3:]  # Extracting cell data values
                    for cell, value in zip(start_cell_columns, values):
                        cell_data[cell].append((timestamp, elapsed_time, float(value)))

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
