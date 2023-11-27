"""
A command-line utility for loading and saving animal data.
The script utilizes the AnimalData class to read data from a specified
input CSV file, process it, and then save the processed data to
an output CSV file.

The script supports command-line arguments to specify the input and
output file paths. It includes error handling to manage issues that
might occur during file processing.

Usage:
    python load_data.py -i <input_file_path> -o <output_file_path>

Arguments:
    -i: Path to the input CSV file containing animal data.
    -o: Path where the processed data will be saved as a CSV file.

This script includes:
    - A function (get_args) to parse the command-line arguments.
    - A main function which orchestrates the loading of data from the input
      file, processing the data using the AnimalData class, and saving it
      to the output file.
"""

from animal_data import AnimalData
import argparse
import sys


def get_args():
    """
    Parses command line arguments using argparse.

    Returns:
        argparse.Namespace: An object containing all command line arguments.
            - 'i': Input file name (str)
            - 'o': Output file name (str)
    """
    parser = argparse.ArgumentParser(description='Parse animal data',
                                     prog='load_data.py')
    parser.add_argument('-i',
                        type=str,
                        help='Input file name',
                        required=True)
    parser.add_argument('-o',
                        type=str,
                        help='Output file name',
                        required=True)
    args = parser.parse_args()

    return args


def main():
    """
    Main function to execute the script. It handles the command line
    arguments for input and output files, loads data from the input CSV file,
    and saves processed data to the output CSV file.

    Raises:
        Exception: Catches and prints any exceptions that occur during
                   file processing.
    """
    try:
        args = get_args()

        input_filename = args.i
        output_filename = args.o

        # Load CSVs
        animal_data = AnimalData.from_csv(str(input_filename))

        # Save time adjusted datasets
        animal_data.save_to_csv(str(output_filename))
        print("CSVs loaded and saved successfully.")

    except Exception as e:  # Replace with more specific exceptions if known
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
