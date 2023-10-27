import csv

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
        return {cell: next((t, v) for t, v in values if t == timestamp) for cell, values in self.cell_data.items()}

    def remap_time_values(self):
        """Remap the timestamps so they start from 0 and increase in fixed intervals."""

        # Assuming consistent time intervals, determine the interval from the first two timestamps
        first_cell = next(iter(self.cell_data.values()))
        time_interval = first_cell[1][0] - first_cell[0][0]

        # Get the starting time from the first data point of the first cell
        start_time = first_cell[0][0]

        # Remap the timestamps in the cell_data dictionary
        for cell, values in self.cell_data.items():
            self.cell_data[cell] = [(t - start_time, v) for t, v in values]

    def save_to_csv(self, output_path):
        """Save the cell data to a CSV file."""
        # Extract headers
        cells = list(self.cell_data.keys())
        headers = ['Time(s)'] + cells

        # Prepare rows
        # Assume all cells have the same number of timestamps; use the first cell as reference
        rows = []
        for i in range(len(self.cell_data[cells[0]])):
            row = [self.cell_data[cells[0]][i][0]]  # Start with the timestamp
            for cell in cells:
                row.append(self.cell_data[cell][i][1])  # Add each cell's value at that timestamp
            rows.append(row)

        # Write data to CSV
        with open(output_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write the header
            writer.writerows(rows)    # Write the data rows

    @classmethod
    def from_csv(cls, filepath):
        """Class method to create an AnimalData instance from a CSV file."""
        animal_num = filepath.split('.')[0]

        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            header = [cell.strip() for cell in header]  # This line is added to remove whitespace
            _ = next(reader)  # Skip the cell status row

            cell_data = {cell: [] for cell in header[1:]}

            for row in reader:
                timestamp = float(row[0])
                for i, value in enumerate(row[1:], 1):
                    cell_data[header[i]].append((timestamp, float(value)))

        return cls(animal_num, cell_data)

    @classmethod
    def from_csv_and_remap(cls, filepath):
        """Class method to create an AnimalData instance from a CSV file and then remap the timestamps."""
        instance = cls.from_csv(filepath)
        instance.remap_time_values()
        return instance
