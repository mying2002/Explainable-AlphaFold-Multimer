All PDB files produced when running AlphaFold-Multimer with the set of 30 selected antigen-antibody multimers studied in this work.

These PDB files, among many other files which we do not use, are generated when running Explainable-AlphaFold-Multimer/slurm_scripts/run_AA_multimer_perturb.sh in Grace and are deposited in the directory Explainable-AlphaFold-Multimer/AA_multimer_garbage_out. One may copy these PDB files from Explainable-AlphaFold-Multimer/AA_multimer_garbage_out to this directory from the command line in Grace with the following commands:

`cd Explainable-AlphaFold-Multimer/AA_multimer_garbage_out`

`cp **/*unrelaxed_rank_001*.pdb ../AA_multimer_all_pdb/`
