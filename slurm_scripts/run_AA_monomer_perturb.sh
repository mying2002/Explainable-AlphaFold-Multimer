#!/bin/bash

#SBATCH --time=5:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --array=1-7

# Ensure that --array has the correct number of jobs

#config=/home/cpsc471_ljm78/final_project/job_array_config_files/test_AA_monomer_config.txt # test 1 job
#config=/home/cpsc471_ljm78/final_project/job_array_config_files/AA_monomer_config.txt # real, 3481 jobs
#config=/home/cpsc471_ljm78/final_project/job_array_config_files/fill1_AA_monomer_config.txt # real, 90 jobs
config=/home/cpsc471_ljm78/final_project/job_array_config_files/fill2_AA_monomer_config.txt # real, 7 jobs

seq_id=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)
seq=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $3}' $config)
delete_index=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $4}' $config)

# Move to the directory where we want the output to go
cd /home/cpsc471_ljm78/final_project/AA_garbage_out

srun python3 /home/cpsc471_ljm78/final_project/python_scripts/alphafold_AA_monomer.py ${seq_id} ${seq} ${delete_index}
