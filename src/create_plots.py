"""
Script to create visualizations for neural activity data.

Functionality for two types of visualizations:
1. Line plot showing neural activity over time.
2. Heatmap visualizing correlation matrix of neural activity.

Usage:
    python this_script_name.py -f data_file.csv -c C000 C001
                               -o output_filename.png -p plot_type

Arguments:
    -f, --file: Path to data CSV (required).
    -c, --cells: List of cell names for the plot (required).
    -o, --output: Filename for the output (default "output.png").
    -p, --plot_type: Type ("line" or "correlation", default "line").
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys

from animal_data import AnimalData
from correlations import correlation_matrix


def create_line_plot(data, cells, output_filename):
    """Generates line plot of neural activity over time for cells."""
    try:
        plt.figure(figsize=(12, 7))
        for cell in cells:
            data_for_cell = data.get_data_for_cell(cell)
            # Check if data_for_cell is empty
            if not data_for_cell:
                raise ValueError(f"Cell not found in data")
            # Unpacking the tuple into three variables
            # We throw away the second value, elapsed time
            timestamps, _, values = zip(*data_for_cell)
            plt.plot(timestamps, values, label=cell)

        plt.xlabel('Timestamp')
        plt.ylabel('Neural Activity Value')
        plt.title('Neural Activity Over Time')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(output_filename)

    except ValueError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print("Could not create line plot")
        sys.exit(1)


def create_correlation_matrix(data, cells, output_filename):
    """Generate heatmap of correlation matrix of neural activity."""
    try:
        # Current Lib function only supports 2 cells, so we check for that
        if len(cells) > 2:
            raise ValueError(f"Only supports 2 cells")

        data_for_cells = [data.get_data_for_cell(cell) for cell in cells]
        # See if any of the cells are not in the data
        if not all(data_for_cells):
            raise ValueError(f"Cell not found in data")

        subset_data = {
            cell: [value for _, _, value in data.get_data_for_cell(cell)]
            for cell in cells
        }
        # Check if subset_data is empty
        if not subset_data:
            raise ValueError(f"No data")

        df = pd.DataFrame(subset_data)

        # We only need the R values, not the p values
        _, corr_matrix = correlation_matrix(df, df)

        # Make numeric and reset the index for plotting
        corr_matrix = corr_matrix.apply(pd.to_numeric, errors="coerce")
        corr_matrix.reset_index(drop=True, inplace=True)

    except ValueError as e:
        sys.stderr.write(e)
        print(e)
        sys.exit(1)
    except Exception as e:
        print("Could not create correlation matrix")
        sys.exit(1)

    plt.figure(figsize=(12, 7))
    sns.heatmap(corr_matrix, annot=True,
                cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Neural Activity')
    plt.tight_layout()
    plt.savefig(output_filename)


def main():
    parser = argparse.ArgumentParser(
        description="Generate visualizations for neural activity data."
    )
    parser.add_argument("-f", "--file", required=True,
                        help="Path to the data CSV file.")
    parser.add_argument("-c", "--cells", nargs='+', required=True,
                        help="List of cell names for the plot.")
    parser.add_argument("-o", "--output", default="../data/output.png",
                        help="Filename for the output.")
    parser.add_argument("-p", "--plot_type", choices=["line", "correlation"],
                        default="line", help="Type of plot to generate.")

    args = parser.parse_args()

    # Load data from CSV with our dataLoader
    data = AnimalData.from_csv(args.file)

    if args.plot_type == "line":
        create_line_plot(data, args.cells, args.output)

    elif args.plot_type == "correlation":
        create_correlation_matrix(data, args.cells, args.output)


if __name__ == "__main__":
    main()
