# Explainable-AlphaFold-Multimer
Repository supplementing the CPSC 471 final project on the explainability of AlphaFold-Multimer

## Detailed instructions on running code

# Setting up local directories
Copy the entire file structure on Github to your local computer.

# Generating configuration files:
Run the notebooks `make_config_files.ipynb` and `AA_make_config_files.ipynb` in Explainable-AlphaFold-Multimer/data_processing. This will generate configuration files in Explainable-AlphaFold-Multimer/config_files which will be used to run AlphaFold and AlphaFold-Multimer on Grace.

# Set up directories on Grace as follows:
The following directories and their subdirectories must be copied from Github to Grace prior to running any code on the cluster:
- Explainable-AlphaFold-Multimer/deletion_perturb_out
- Explainable-AlphaFold-Multimer/garbage_out
- Explainable-AlphaFold-Multimer/python_scripts
- Explainable-AlphaFold-Multimer/config_files
- Explainable-AlphaFold-Multimer/slurm_scripts

# Running AlphaFold and AlphaFold-Multimer on Grace
Once the file structure has been set up, 

Mirdita, M., Schütze, K., Moriwaki, Y. et al. ColabFold: making protein folding accessible to all. Nat Methods 19, 679–682 (2022). https://doi.org/10.1038/s41592-022-01488-1
