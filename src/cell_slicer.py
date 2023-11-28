import pandas as pd
import numpy as np
from animal_data import AnimalData as ad
import df_utils
import argparse
import sys


def cell_query(r_data, query, p_data=None, x_percent=None, alpha=0.05):
    """
    sorts correlation cell pairs and returns list of cell pairs based on query
    query can be either based on significance or the top x percent of r values
    Args:
        r_data: correlation dataframe of r values
        query: sig or top, string of sorting method
        p_data: dataframe of correlation p values, default None
        x_percent: top percent to slice, int, default None
        alpha: significance cutoff, default 0.05
    Returns:
        cell_pairs: list of cell pair tuples of string cell names
        sorted_matrix: series of sorted r values from correlation matrix
        sorted_p_matrix: series of sorted p values from correlation matrix
            if query is top this is returned as None
    """
    try:
        # Convert to 1-D series and drop Null values
        unique_corr_pairs = r_data.unstack().dropna()
        # Sort corr pairs, need to keep values but sort based on absolute value
        order = unique_corr_pairs.abs().sort_values(ascending=False)
        ind = order.index
        sorted_matrix = unique_corr_pairs[ind]
        # python dicts are now sorted so this works to keep sorted order
        sorted_cell_pairs = sorted_matrix.keys()
    except TypeError:
        print('r_data matrix not numbers')
        return None

    # slice based on correlation signinficance:
    if query == 'sig':
        if p_data is None:
            print('Error if query is sig must input p_data')
            return None
        else:
            #  also sorting p values
            p_unique_corr_pairs = p_data.unstack().dropna()
            p_sorted_matrix = p_unique_corr_pairs.sort_values()
            p_sorted_cell_pairs = p_sorted_matrix.keys()

            try:
                #  making slice of series based on alpha
                sig_cell_pairs = p_sorted_matrix.loc[:, p_sorted_matrix.loc[:]
                                                     < alpha]
                #  getting the cell pair names into a list
                x_len = len(sig_cell_pairs)
                cell_pairs = []
                for i in range(x_len):
                    cells = p_sorted_cell_pairs[i]
                    cell_pairs.append(cells)
                return cell_pairs, sorted_matrix, p_sorted_matrix
            except TypeError:
                print('p_data matrix not numbers')
                return None

    #  slice based on top x percent
    elif query == 'top':
        if x_percent is None:
            print('Error if query is top must input x_per')
            return None
        else:
            #  turing int into float percentage
            per = x_percent/100
            cells_length = len(sorted_cell_pairs)
            #  have to round to a int number of pairs
            x_len = round(cells_length*per)
            if x_len == 0:
                print('percent is too low to round to 1 pair')
            cell_pairs = []
            for i in range(x_len):
                cells = sorted_cell_pairs[i]
                cell_pairs.append(cells)
            return cell_pairs, sorted_matrix, None

    else:
        print('Error query must be sig or top')
        return None


def get_slice_args():
    """arg parser for cell_query function and cell_slicer.py"""
    parser = argparse.ArgumentParser(description="Args for cell_slicer.")
    parser.add_argument("-f", "--file_name", type=str, required=True,
                        help="file name/path of correlation matrix r values")
    parser.add_argument('-o', '--out_file', type=str,
                        help='path/name for cell pairs output file',
                        required=True)
    parser.add_argument('-s', '--sorted_out_file', type=str,
                        help='path/name for sorted corr matrix output file',
                        required=True)
    parser.add_argument('-q', '--query', type=str,
                        help='sig or top', required=True)
    parser.add_argument("-p", "--file_pvals", type=str, required=False,
                        help="file path/name of correlation matrix p values")
    parser.add_argument("-x", "--x_percent", type=int, required=False,
                        help="specify x percent value (int)")
    parser.add_argument("-a", "--alpha", type=float, default=0.05,
                        help="significance cutoff, defalt=0.05")
    parser.add_argument('--out_pvals', type=str, required=False,
                        help='path/name for sorted p values output file')
    args = parser.parse_args()
    return args


def main():
    args = get_slice_args()
    #  load correlation data frames
    try:
        r_data = pd.read_csv(args.file_name, index_col=0)
        if args.file_pvals is not None:
            p_data = pd.read_csv(args.file_pvals, index_col=0)
        else:
            p_data = None
    except FileNotFoundError:
        print('Error: Could not find ' + args.file_name
              + ' &/or ' + args.file_pvals)
        sys.exit(1)
    except PermissionError:
        print('Error: Could not open ' + args.file_name
              + ' &/or ' + args.file_pvals)
        sys.exit(1)

    try:
        cell_pairs, sorted_matrix, sorted_p_values = cell_query(r_data,
                                                            args.query,
                                                            p_data,
                                                            args.x_percent,
                                                            args.alpha)

    except TypeError:  # when returning None (1) vs 3 things it's TypeError
        print('Error above prevented cell_pairs file production.')
        sys.exit(1)

    #  save cell pairs as .txt file
    f = open(args.out_file, 'w')
    for e in cell_pairs:
        f.write(str(e) + '\n')
    f.close()
    sorted_df = pd.DataFrame(sorted_matrix)
    sorted_df.to_csv(args.sorted_out_file)
    if sorted_p_values is not None:
        pvals_df = pd.DataFrame(sorted_p_values)
        pvals_df.to_csv(args.out_pvals)


if __name__ == '__main__':
    main()
