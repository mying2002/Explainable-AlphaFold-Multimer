All PDB files produced when running AlphaFold with the set of 30 selected multimers studied in this work.

Note that do to the sheer number of files that will be deposited in this directory, we do not put the files on Github. One can generate them with Grace.

These PDB files, among many other files which we do not use, are generated when running Explainable-AlphaFold-Multimer/slurm_scripts/run_multimer_perturb.sh in Grace and are deposited in the directory Explainable-AlphaFold-Multimer/multimer_garbage_out. One may copy these PDB files from Explainable-AlphaFold-Multimer/multimer_garbage_out to this directory from the command line in Grace with the following commands:

`cd Explainable-AlphaFold-Multimer/multimer_garbage_out`

`cp **/*unrelaxed_rank_001*.pdb ../multimer_all_pdb/`
