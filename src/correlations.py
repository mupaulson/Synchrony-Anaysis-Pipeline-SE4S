import pandas as pd
import numpy as np
import scipy.stats as sps
import argparse
from animal_data import AnimalData as ad
import sys


# Generate correlation matrix
def correlation_matrix(dataframe1, dataframe2):
    """
    Takes two dataframes of cell data and correlates all cells
    between the dataframes. Outputs two dataframes of p-values
    and R values for every correlation. Different size dataframes
    are cut to be the same length, and missing data is removed.
        Args: dataframe1, dataframe2 are the two dataframes to
        correlate. The cell names of dataframe1 will be the
        index of the output, and the cells in dataframe2 will be
        the column names.
        """
    data1 = dataframe1
    data2 = dataframe2

    col1 = [c for c in data1.columns.values]
    col2 = [c for c in data2.columns.values]

    # convert columns to numpy to correlate
    # if all values in the column are the same NaN values will be returned
    corr_p = pd.DataFrame(data=[], index=col1, columns=col2)
    corr_r = pd.DataFrame(data=[], index=col1, columns=col2)

    # cut off extra data from end so dataframes can be the same length
    len1 = len(data1)
    len2 = len(data2)

    if len1 != len2:
        if len1 > len2:
            data1 = data1.iloc[:len2]
            print('dataframe 1 too long - cut off to match')
        elif len2 > len1:
            data2 = data2.iloc[:len1]
            print('dataframe 2 too long - cut off to match')
        else:
            print('error matching lengths')
            sys.exit(1)

    for c1 in col1:
        for c2 in col2:
            a1 = data1[c1].astype(float)
            a2 = data2[c2].astype(float)

            # drop times where 1 value is nan/missing from either array
            a1 = a1[~np.isnan(a2)]
            a2 = a2[~np.isnan(a1)]

            a1 = a1[~np.isnan(a1)]
            a2 = a2[~np.isnan(a2)]

            try:
                (r, p) = sps.pearsonr(a1, a2)
            except:  # noqa
                print('unable to calculate correlation')
                sys.exit(1)

            corr_p.loc[c1, c2] = p
            corr_r.loc[c1, c2] = r

    return corr_p, corr_r


# define parser for help with the get_column function
def get_args():
    parser = argparse.ArgumentParser(
                                description='correlates two dataframes',
                                prog='correlation_matrix')
    parser.add_argument('--dataframe1',
                        help='pass 1 dataframe')
    parser.add_argument('--dataframe2',
                        help='pass second dataframe')
    parser.add_argument('--out_file_r',
                        help='name list for output file r values')
    parser.add_argument('--out_file_p',
                        help='name list for output file p values')
  
    args = parser.parse_args()
    return args


# define main function
def main():
    args = get_args()

    df1_file = args.dataframe1
    df2_file = args.dataframe2

    df1 = pd.read_csv(df1_file)
    df2 = pd.read_csv(df2_file)

    corr_p, corr_r = correlation_matrix(df1, df2)

    r_file_out = args.out_file_r
    p_file_out = args.out_file_p

    corr_r.to_csv(r_file_out)
    corr_p.to_csv(p_file_out)



if __name__ == '__main__':
    main()
