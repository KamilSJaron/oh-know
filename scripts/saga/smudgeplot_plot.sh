#!/bin/bash

#SBATCH --job-name=KMCdb
#SBATCH --account=NN9458K
#SBATCH --time=00-04:00:00
#SBATCH --cpus-per-task=8 
#SBATCH --mem-per-cpu=10000M


KMER_PAIRS=$1
# output prefix
OUTPUT_PREFIX=$2

module --force purge
module load Miniconda3/4.9.2
conda init bash
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
source ~/.bashrc

conda activate /cluster/projects/nn9458k/oh_know/.conda/kmer_tools

smudgeplot.py plot -o "$OUTPUT_PREFIX" "$KMER_PAIRS"
