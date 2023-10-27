from animal_data import AnimalData

THRESHOLD = 0.01 # 1/100 of a second

def adjust_timestamps(data1, data2):
    """Adjust timestamps of the two datasets if they are within the threshold."""
    if len(data1.cell_data["C000"]) != len(data2.cell_data["C000"]):
        raise ValueError("Datasets have mismatched lengths.")
    
    # Assume that both datasets have the same number of timestamps
    for i in range(len(data1.cell_data["C000"])):  # Using 'C000' as a reference for timestamps
        timestamp1 = data1.cell_data["C000"][i][0]
        timestamp2 = data2.cell_data["C000"][i][0]

        if abs(timestamp1 - timestamp2) <= THRESHOLD:
            # Set them to the average, rounded to nearest 0.01
            avg_timestamp = round((timestamp1 + timestamp2) / 2, 2)

            # Update the timestamps in both datasets
            for cell in data1.cell_data:
                t, v = data1.cell_data[cell][i]
                data1.cell_data[cell][i] = (avg_timestamp, v)
            for cell in data2.cell_data:
                t, v = data2.cell_data[cell][i]
                data2.cell_data[cell][i] = (avg_timestamp, v)

def main():
    # Load and remap CSVs
    animal1_data = AnimalData.from_csv_and_remap("../data/4659-test2.csv")
    animal2_data = AnimalData.from_csv_and_remap("../data/4807-test2.csv")

    # Adjust their timestamps
    adjust_timestamps(animal1_data, animal2_data)

    # Save time adjusted datasets
    animal1_data.save_to_csv("../data/4659-test2-remap.csv")
    animal2_data.save_to_csv("../data/4807-test2-remap.csv")

    print("CSVs remapped and saved successfully.")

if __name__ == "__main__":
    main()