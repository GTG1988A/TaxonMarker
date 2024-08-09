#!/usr/bin/env python

import argparse
import re

__author__ = 'Gabryelle Agoutin - INRAE'
__copyright__ = 'Copyright (C) 2024 INRAE'
__license__ = 'GNU General Public License'
__version__ = '1.0'
__email__ = 'gabryelle.agoutin@inrae.fr'
__status__ = 'prod'

def filter_lines_by_keywords(seq_file, output_file, include_keywords=None, exclude_keywords=None, log_file=None):
    """Filter lines based on required and excluded keywords in taxonomy."""
    
    filtered_lines = []
    rejected_lines = []
    
    with open(seq_file, 'r') as infile:
        for line in infile:
            if line.startswith('>'):
                taxonomy_match = re.search(r"taxid=\d+; (.*)", line)
                if taxonomy_match:
                    taxonomy = taxonomy_match.group(1)
                    include = include_keywords and any(keyword in taxonomy for keyword in include_keywords)
                    exclude = exclude_keywords and any(keyword in taxonomy for keyword in exclude_keywords)
                    
                    if include and not exclude:
                        filtered_lines.append(line)
                    else:
                        rejected_lines.append(line)
            else:
                filtered_lines.append(line)
    
    # Write the filtered lines to the output file
    with open(output_file, 'w') as outfile:
        for line in filtered_lines:
            outfile.write(line)
    
    # Write the rejected lines to the log file if provided
    if log_file:
        with open(log_file, 'w') as log:
            log.write("Rejected lines:\n")
            for line in rejected_lines:
                log.write(line)
    
    return filtered_lines

def extract_genome_names(filtered_file, genome_names_file):
    """Extract genome names from the filtered file and write them to a separate file."""
    
    genome_names = set()
    
    with open(filtered_file, 'r') as infile:
        for line in infile:
            if line.startswith('>'):
                genome_name = re.match(r'>([^|]+)\|', line)
                if genome_name:
                    genome_names.add(genome_name.group(1))
    
    with open(genome_names_file, 'w') as outfile:
        for name in sorted(genome_names):
            outfile.write(f"{name}\n")

def main():
    parser = argparse.ArgumentParser(description="Filter lines in a sequence file based on taxonomy, generate a filtered output file, log rejected lines, and extract genome names.")
    parser.add_argument("-s", "--seq_file", type=str, required=True, help="Input file containing sequences with taxonomy (e.g., name_seq_with_taxo.txt).")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Output file for the filtered sequences (e.g., filtered_seq_with_taxo.txt).")
    parser.add_argument("-i", "--include_keywords", type=str, nargs='*', help="Keywords that must be present in taxonomy to keep a line (e.g., f__Lactobacillaceae).")
    parser.add_argument("-e", "--exclude_keywords", type=str, nargs='*', help="Keywords that, if present, will cause a line to be excluded (e.g., g__Leuconostoc).")
    parser.add_argument("-l", "--log_file", type=str, help="Output file to log rejected lines (optional).")
    args = parser.parse_args()

    # Filter lines based on inclusion and exclusion keywords
    filtered_lines = filter_lines_by_keywords(
        args.seq_file,
        args.output_file,
        include_keywords=args.include_keywords,
        exclude_keywords=args.exclude_keywords,
        log_file=args.log_file
    )

    # Generate genome names file
    genome_names_file = 'genome_name_selected.txt'
    extract_genome_names(
        args.output_file,
        genome_names_file
    )

    print(f"Filtered lines written to {args.output_file}")
    print(f"Genome names written to {genome_names_file}")
    if args.log_file:
        print(f"Rejected lines logged to {args.log_file}")

if __name__ == "__main__":
    main()