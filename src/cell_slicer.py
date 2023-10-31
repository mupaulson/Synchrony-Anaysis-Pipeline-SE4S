import pandas as pd
import numpy as np
from animal_data import AnimalData as ad
import df_utils
import argparse
import sys


# from cell_slicer.py
def cell_query(r_data, query, p_data=None, x_per=None, alpha=0.05):

    # Convert to 1-D series and drop Null values 
    unique_corr_pairs = r_data.unstack().dropna()

    # Sort correlation pairs, need to keep values but sort based on absolute value 
    order = unique_corr_pairs.abs().sort_values(ascending = False)
    ind = order.index
    sorted_mat = unique_corr_pairs[ind] 
    # sorted cell pairs, python dicts are now sorted so this works to keep sorted order
    sorted_cps =sorted_mat.keys()
    # slice based on correlation signinficance:
    if query == 'sig':
        if p_data is None:
            print('Error: if query is sig must input p_data')
            return None
        if alpha is None:
            print('Error: if query is sig must input a')
            return None
        else:
            try:
                # Convert to 1-D series and drop Null values 
                p_unique_corr_pairs = p_data.unstack().dropna() 

                # Sort correlation pairs 
                p_sorted_mat = p_unique_corr_pairs.sort_values()
                # sorted cell pairs, python dicts are now sorted so this works to keep sorted order
                p_sorted_cps =sorted_mat.keys()
                sig_cell_pairs = p_sorted_mat.loc[:, p_sorted_mat.loc[:] < alpha] 
                x_len = len(sig_cell_pairs)
                cell_pairs = []
                for i in range(x_len):
                    cells= sorted_cps[i]
                    cell_pairs.append(cells)
                return cell_pairs, sorted_mat, p_sorted_mat
            except:
                print('some error happened here')
                return None
                
    #  slice based on top x percent
    elif query == 'top':
        if x_per is None:
            print('Error: if query is top must input x_per')
            return None
        else:
            per = x_per/100
            l = len(sorted_cps)
            x_len = round(l*per)
            print(l)
            print(x_len)
            cell_pairs = []
            for i in range(x_len):
                cells= sorted_cps[i]
                cell_pairs.append(cells)
            return cell_pairs, sorted_mat
            
    else:
        print('Error: query must be sig or top')
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Slice correlation data by query. Saves 2d list of cell pairs as out_file."
    )
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
    parser.add_argument("-a", "--alpha", type=float, defalut=0.05, required=False,
                        help="significance cutoff, defalt=0.05") #does defalt and required=false work?
    args = parser.parse_args()
    
    #  load correlation data frames
    try:
        r_data = pd.read_csv(args.file_name)
        if args.file_pvals != None:
            p_data = pd.read_csv(args.file_pvals)
        else:
            p_data = None
    except FileNotFoundError:
        print('Error: Could not find ' + args.file_name
              + ' &/or ' + args.file_pvals)
        sys.exit(1)
    except PermissionError:
        print('Error: Could not find ' + args.file_name
              + ' &/or ' + args.file_pvals)
        sys.exit(1)
    
    cell_pairs, sorted_matrix = cell_query(r_data, args.query, p_data, args.x_percent)
    
    if cell_pairs is None:
        print('Error above prevented cell_pairs file production.')
        sys.exit(1)
    else:
        #  save cell pairs as .txt file
        f = open(args.out_file, 'w')
        for e in cell_pairs:
            f.write(str(e) + '\n')
        f.close()
    
    sorted_df = pd.DataFrame(sorted_matrix)
    sorted_df.to_csv(args.sorted_out_file)


if __name__ == '__main__':
    main()
   