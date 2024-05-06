#!/bin/bash

#SBATCH --time=0:30:00
#SBATCH --mem-per-cpu=10G

# Move to the directory where we want the params folder to go
cd /home/cpsc471_ljm78/final_project

srun python3 /home/cpsc471_ljm78/final_project/python_scripts/alphafold_download_params.py
