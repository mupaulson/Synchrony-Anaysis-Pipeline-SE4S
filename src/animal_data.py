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
    
    def remap_time_values(self):
        """Remap the timestamps so they start from 0 and round to the nearest 1/100 second."""

        first_timestamp = self.cell_data["C000"][0][0] # the first timestamp
        # Remap the timestamps in the cell_data dictionary
        for cell, values in self.cell_data.items():
            new_values = []
            for t, v in values:
                adjusted_timestamp = round(t - first_timestamp, 2)
                new_values.append((adjusted_timestamp, v))
            self.cell_data[cell] = new_values

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