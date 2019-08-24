#!/bin/bash

#SBATCH --job-name=geneology
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=16GB
#SBATCH --time=12:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=cs2737@nyu.edu
  
module purge
module load python3/intel/3.6.3

python3 students_scrape.py
