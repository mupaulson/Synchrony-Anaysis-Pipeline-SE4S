import pandas as pd
import numpy as np
from animal_data import AnimalData as ad
import df_utils
import argparse


def normalize_df(ani_data):
    """
    Normalizes cell df/f data by dividing each cell column
    by the max value in each column so that each cells max
    value in the normalized df is 1.
    Arg: ani_data- data from session in AnimalData 
         class structure
    Returns: dfn, a dataframe of normalized data
    """
    cells = ani_data.cell_data.keys()
    df = df_utils.animal_data_to_df(ani_data, cells)
    m = np.max(df)
    dfn= pd.DataFrame()
    cols = df.columns
    for i in range (len(cols)):
        dfn[cols[i]] = (df[cols[i]]/m[i]) #this line is throwing warnings like crazy, try to figure out someting better
    return dfn

def main():
    
    parser = argparse.ArgumentParser(
        description="Normalize data."
    )
    parser.add_argument("-f", "--file_name", type=str, required=True,
                        help="file name/path of data")
    parser.add_argument('-o', '--out_file', type=str,
                        help='path/name for output file',
                        required=True)
    args = parser.parse_args()

    #  pull un-normalized df from animal data
    ani_data = ad.AnimalData(args.file_name)
    norm_df = normalize_df(ani_data)
    norm_df.to_csv(args.out_file)


if __name__ == '__main__':
    main()
