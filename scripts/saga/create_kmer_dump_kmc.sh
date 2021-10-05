#!/bin/bash

#SBATCH --job-name=KMCdump
#SBATCH --account=NN9458K
#SBATCH --time=00-02:00:00
#SBATCH --cpus-per-task=1 
#SBATCH --mem-per-cpu=10000M


module --force purge
module load Miniconda3/4.9.2
conda init bash
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
source ~/.bashrc

KMER_DB=$1
MIN_COV=$2
MAX_COV=$3
OUTPUT_DUMP=$4

conda activate /cluster/projects/nn9458k/oh_know/.conda/kmer_tools

kmc_tools transform $KMER_DB -ci"$MIN_COV" -cx"$MAX_COV" dump -s <output_name.dump>
kmc_dump -ci"$MIN_COV" -cx"$MAX_COV" "$KMER_DB" "$OUTPUT_DUMP"
