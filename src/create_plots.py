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

from animal_data import AnimalData

def create_line_plot(data, cells, output_filename):
    """Generates line plot of neural activity over time for cells."""
    plt.figure(figsize=(12, 7))
    for cell in cells:
        data_for_cell = data.get_data_for_cell(cell)
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


def create_correlation_matrix(data, cells, output_filename):
    """Generate heatmap of correlation matrix of neural activity."""
    subset_data = {
        cell: [value for _, _, value in data.get_data_for_cell(cell)]
        for cell in cells
    }
    # Create dataframe to get easy correlation matrix functionality
    df = pd.DataFrame(subset_data)
    correlation_matrix = df.corr()

    plt.figure(figsize=(12, 7))
    sns.heatmap(correlation_matrix, annot=True,
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
