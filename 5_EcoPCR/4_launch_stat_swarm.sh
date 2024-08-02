#!/bin/bash
#SBATCH -J launch_format_ecoPCR_result
#SBATCH -p unlimitq
#SBATCH --mem=50G
#SBATCH -c 3
#SBATCH --mail-type=BEGIN,END,FAIL

module load devel/python/Python-3.11.1

python stats_report.py -c cluster.txt -t all_modified.fna -o stats.txt -i f__Lactobacillaceae -e g__Leuconostoc g__Pediococcus g__Oenococcus g__Unassigned sp. g__Weissella g__Dellaglioa g__Periweissella g__Convivina -l rejected_clusters.txt -r cluster_corrected.txt

