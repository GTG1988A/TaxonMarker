#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

__author__ = 'Gabryelle Agoutin - INRAE'
__copyright__ = 'Copyright (C) 2024 INRAE'
__license__ = 'GNU General Public License'
__version__ = '1.0'
__email__ = 'gabryelle.agoutin@inrae.fr'
__status__ = 'prod'

def load_data(file_name):
    """Load data from a text file into a set.

    Args:
        file_name (str): The path to the text file.

    Returns:
        set: A set containing the unique lines from the file.
    """
    with open(file_name, 'r') as file:
        return set(line.strip() for line in file)

def create_venn_diagrams(data, output_file):
    """Create and save Venn diagrams with descriptions.

    Args:
        data (dict): A dictionary with file names as keys and sets of data as values.
        output_file (str): The path to the output image file.
    """
    # Create figure and subplots
    fig, axs = plt.subplots(1, 2, figsize=(16, 8))  # 1 row, 2 columns
    fig.subplots_adjust(wspace=0.4, left=0.05, right=0.95, top=0.85, bottom=0.2)  # Adjust margins and spacing

    # Diagram for uniq_taxo.txt and uniq_taxo_16S.txt
    venn2([data['uniq_taxo.txt'], data['uniq_taxo_16S.txt']],
          set_labels=('target gene', '16S gene'),
          ax=axs[0])
    axs[0].set_title('Caught species comparison')
    
    # Description below the first diagram
    axs[0].text(0.5, -0.2, 
                'This diagram compares the species caught by the target gene with those detected by the 16S gene.\n'
                'Red represents species detected only by the target gene.\n'
                'Green represents species detected only by the 16S gene.\n'
                'Yellow represents species detected by both genes.',
                ha='center', va='top', fontsize=10, transform=axs[0].transAxes, bbox=dict(facecolor='white', alpha=0.7))

    # Diagram for uniq_taxo_good_discriminated.txt and uniq_taxo_good_discriminated_16S.txt
    venn2([data['uniq_taxo_good_discriminated.txt'], data['uniq_taxo_good_discriminated_16S.txt']],
          set_labels=('target gene', '16S gene'),
          ax=axs[1])
    axs[1].set_title('Species correctly discriminated')

    # Description below the second diagram
    axs[1].text(0.5, -0.2, 
                'This diagram shows the species that were correctly discriminated by the target gene and the 16S gene.\n'
                'Red represents species correctly discriminated only by the target gene.\n'
                'Green represents species correctly discriminated only by the 16S gene.\n'
                'Yellow represents species correctly discriminated by both genes.',
                ha='center', va='top', fontsize=10, transform=axs[1].transAxes, bbox=dict(facecolor='white', alpha=0.7))

    # Save the figure to a file
    plt.savefig(output_file, bbox_inches='tight')  # Use bbox_inches='tight' to fit the layout
    print(f"Venn diagrams with descriptions saved to '{output_file}'")

def main():
    parser = argparse.ArgumentParser(
        description='Create Venn diagrams comparing species data.',
        epilog='Example: python script_name.py --taxo_target_gene path/to/uniq_taxo.txt --taxo_16S_gene path/to/uniq_taxo_16S.txt --good_discrimination_target_gene path/to/uniq_taxo_good_discriminated.txt --good_discrimination_16S path/to/uniq_taxo_good_discriminated_16S.txt --output path/to/output_image.png'
    )
    
    # Define arguments
    parser.add_argument('--taxo_target_gene', required=True, help='Path to the uniq_taxo.txt file')
    parser.add_argument('--taxo_16S_gene', required=True, help='Path to the uniq_taxo_16S.txt file')
    parser.add_argument('--good_discrimination_target_gene', required=True, help='Path to the uniq_taxo_good_discriminated.txt file')
    parser.add_argument('--good_discrimination_16S', required=True, help='Path to the uniq_taxo_good_discriminated_16S.txt file')
    parser.add_argument('--output', required=True, help='Path to the output image file')

    # Parse arguments
    args = parser.parse_args()

    # Load data from files
    data = {
        'uniq_taxo.txt': load_data(args.taxo_target_gene),
        'uniq_taxo_16S.txt': load_data(args.taxo_16S_gene),
        'uniq_taxo_good_discriminated.txt': load_data(args.good_discrimination_target_gene),
        'uniq_taxo_good_discriminated_16S.txt': load_data(args.good_discrimination_16S)
    }

    # Create Venn diagrams
    create_venn_diagrams(data, args.output)

if __name__ == '__main__':
    main()
