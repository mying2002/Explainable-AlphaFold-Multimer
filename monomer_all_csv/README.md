All csv files produced when running AlphaFold with the set of 45 selected monomers that make up the multimers studied in this work.

Note that do to the sheer number of files that will be deposited in this directory, we do not put the files on Github. One can generate them with Grace.

These csv files, among many other files which we do not use, are generated when running Explainable-AlphaFold-Multimer/slurm_scripts/run_monomer_perturb.sh in Grace and are deposited in the directory Explainable-AlphaFold-Multimer/monomer_garbage_out. One may copy these csv files from Explainable-AlphaFold-Multimer/monomer_garbage_out to this directory from the command line in Grace with the following commands:

`cd Explainable-AlphaFold-Multimer/monomer_garbage_out`

`cp **/*.csv ../monomer_all_csv/`
