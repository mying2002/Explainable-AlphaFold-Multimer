#!/bin/bash

#SBATCH --time=4:00:00
#SBATCH --mem-per-cpu=6G
#SBATCH --array=1-3576

# Ensure that --array has the correct number of jobs

config=/home/cpsc471_ljm78/final_project/job_array_config_files/monomer_config.txt

seq=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)
delete_index=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $3}' $config)

# Move to the directory where we want the output to go
cd /home/cpsc471_ljm78/final_project/garbage_out

srun python3 /home/cpsc471_ljm78/final_project/python_scripts/alphafold_monomer.py ${seq} ${delete_index}
