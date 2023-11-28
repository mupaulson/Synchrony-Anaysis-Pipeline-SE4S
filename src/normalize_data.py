import pandas as pd
import numpy as np
from animal_data import AnimalData as ad
import df_utils
import argparse


def normalize_df(ani_data, cells=None):
    """
    Normalizes cell df/f data by dividing each cell column
    by the max value in each column so that each cells max
    value in the normalized dataframe is 1.
    Args:
        ani_data: data from session in AnimalData
             class structure
        cells: list of cells names (str) to normalize,
            defalt=None will normalize all cells in dataset
    Returns: dfn, a dataframe of normalized data
    """
    if cells is None:
        cells = ani_data.cell_data.keys()
    df = df_utils.animal_data_to_df(ani_data, cells)
    if df is None:
        print('unable to normalize data if unable to convert to dataframe')
        return None
    try:
        max_values = df.max(axis=0)
        dfn = df / max_values
        return dfn
    except TypeError:
        print('df values are not numbers')
        return None


def main():

    parser = argparse.ArgumentParser(description="Normalize data.")
    parser.add_argument("-f", "--file_name", type=str, required=True,
                        help="file name/path of data")
    parser.add_argument('-o', '--out_file', type=str,
                        help='path/name for output file',
                        required=True)
    args = parser.parse_args()

    #  pull un-normalized df from animal data structure
    ani_data = ad.from_csv(args.file_name)
    norm_df = normalize_df(ani_data)
    if norm_df is None:
        print('error above prevented saving of normalized csv')
        sys.exit(1)
    norm_df.to_csv(args.out_file, index=False)


if __name__ == '__main__':
    main()
