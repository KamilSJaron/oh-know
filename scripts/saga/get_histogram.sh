#!/bin/bash

#SBATCH --job-name=KMCdb
#SBATCH --account=NN9458K
#SBATCH --time=00-00:30:00
#SBATCH --cpus-per-task=1 
#SBATCH --mem-per-cpu=5000M

KMER_DB=$1
OUT_HIST=$2

module purge
module load Miniconda3/4.9.2
conda init bash
source ~/.bashrc

conda activate /cluster/projects/nn9458k/oh_know/.conda/kmer_tools

kmc_tools transform $KMER_DB histogram $OUT_HIST -cx100000

