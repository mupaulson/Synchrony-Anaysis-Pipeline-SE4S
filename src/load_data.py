from animal_data import AnimalData
import argparse
import sys

def get_args():
    """ Returns arguments passed through the command line.

    Parameters
    ----------
    None

    Returns
    -------
    args:   argparse.Namespace
            All of the arguments passed through the command line
             
    """
    parser = argparse.ArgumentParser(description='Parse animal data',
                                    prog='load_data.py')
    parser.add_argument('-i',
                        type=str,
                        help='Input file name',
                        required=True)
    parser.add_argument('-r',
                        action='store_true',
                        help='Remap time values',
                        required=False)
    parser.add_argument('-o',
                        type=str,
                        help='Output file name',
                        required=True)
    args = parser.parse_args()

    return args

def main():
    args = get_args()

    input_filename = args.i
    remap = args.r
    output_filename = args.o

    # Load CSVs
    animal_data = AnimalData.from_csv(str(input_filename))

    # Adjust the timestamps
    if remap:
        animal_data.remap_time_values()

    # Save time adjusted datasets
    animal_data.save_to_csv(str(output_filename))
    print("CSVs remapped and saved successfully.")

if __name__ == "__main__":
    main()