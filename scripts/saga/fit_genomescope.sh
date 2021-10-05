#!/bin/bash

#SBATCH --job-name=fit_genomescope
#SBATCH --account=NN9458K
#SBATCH --time=00-00:20:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=500M

HIST=$1
OUTDIR=$2
NAME=$3
PLOIDY=$4

module purge
module load Miniconda3/4.9.2
conda init bash
source ~/.bashrc

conda activate /cluster/projects/nn9458k/oh_know/.conda/kmer_tools

genomescope.R -p $PLOIDY -i $HIST -o $OUTDIR -n $NAME
