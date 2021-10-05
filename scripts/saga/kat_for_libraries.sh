#!/bin/bash

#SBATCH --job-name=KATcomp
#SBATCH --account=NN9458K
#SBATCH --time=00-02:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=12G

#path and patterns of fastq files of samples 1 and 2 (e.g. reads/Glossina_12)
SAMPLE1=$1
SAMPLE2=$2
# the prefix for the output
OUTPUT_PREFIX=$3

#setting up our environment
module purge
module add KAT/2.4.2-foss-2019a-Python-3.7.2 

#running KAT comp
kat comp -t 8 -o "$OUTPUT_PREFIX" \
"$SAMPLE1*.fastq.gz" "$SAMPLE2*.fastq.gz" 

exit
