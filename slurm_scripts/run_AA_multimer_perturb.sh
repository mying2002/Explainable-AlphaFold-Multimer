#!/bin/bash

#SBATCH --time=3:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --array=1-3466

# Ensure that --array has the correct number of jobs

config = ../config_files/AA_multimer_config.txt # real, 3466 jobs

seq1_id=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)
seq2_id=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $3}' $config)
seq1=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $4}' $config)
seq2=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $5}' $config)
which_seq=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $6}' $config)
delete_index=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $7}' $config)

# Move to the directory where we want the output to go
cd ../garbage_out/AA_multimer_garbage_out

srun python3 ../python_scripts/alphafold_AA_multimer.py ${seq1_id} ${seq2_id} ${seq1} ${seq2} ${which_seq} ${delete_index}
