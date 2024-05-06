#!/bin/bash

#SBATCH --time=0:30:00
#SBATCH --mem-per-cpu=10G

# Move to the directory where we want the params folder to go
cd ..

srun python3 ../python_scripts/alphafold_download_params.py
