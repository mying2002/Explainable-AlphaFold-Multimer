# Explainable-AlphaFold-Multimer
Repository supplementing the CPSC 471 final project on the explainability of AlphaFold-Multimer

# Detailed instructions on running code

## Setting up local directories
Copy the entire file structure on Github to your local computer.

## Generating configuration files:
Run the notebooks `make_config_files.ipynb` and `AA_make_config_files.ipynb` in Explainable-AlphaFold-Multimer/data_processing. This will generate configuration files in Explainable-AlphaFold-Multimer/config_files which will be used to run AlphaFold and AlphaFold-Multimer on Grace.

## Set up directories on Grace as follows:
The following directories and their subdirectories must be copied from Github to Grace prior to running any code on the cluster:
- Explainable-AlphaFold-Multimer/deletion_perturb_out
- Explainable-AlphaFold-Multimer/garbage_out
- Explainable-AlphaFold-Multimer/python_scripts
- Explainable-AlphaFold-Multimer/config_files
- Explainable-AlphaFold-Multimer/slurm_scripts

## Running AlphaFold and AlphaFold-Multimer on Grace
Once the file structure has been set up, follow these two steps to run AlphaFold and AlphaFold-Multimer on Grace:
1. Install the weights for AlphaFold by running the script `download_params.sh`. This can be done from the command line with `sbatch download_params.sh` while in the directory Explainable-AlphaFold-Multimer/slurm_scripts.
2. Once the parameters have been downloaded, you may execute the following commands while in Explainable-AlphaFold-Multimer/slurm_scripts:
- `sbatch run_monomer_perturb.sh` (to run AlphaFold on the selected generic mononumeric sequences)
- `sbatch run_multimer_perturb.sh` (to run AlphaFold-Multimer on the selected generic multinumeric sequences)
- `sbatch run_AA_monomer_perturb.sh` (to run AlphaFold on the selected antibody/antigen mononumeric sequences)
- `sbatch run_AA_multimer_perturb.sh` (to run AlphaFold-Multimer on the selected antibody-antigen multinumeric sequences)
Since each of these scripts may submit several thousand processes on the cluster to run in parallel, we recommend running the scripts separately, waiting for all jobs submitted via one script to finish before sbatching the next one.

## Copying outputs to local directory
Copy the outputs from running AlphaFold and AlphaFold-Multimer on the cluster to your local computer with:

- `scp /grace/path/to/deletion_perturb_out/monomer_output.csv /path/to/local/Explainable-AlphaFold-Multimer/deletion_perturb_out/monomer_output.csv`

- `scp /grace/path/to/deletion_perturb_out/multimer_output.csv /path/to/local/Explainable-AlphaFold-Multimer/deletion_perturb_out/multimer_output.csv`

- `scp /path/to/deletion_perturb_out/AA_monomer_output.csv /path/to/local/Explainable-AlphaFold-Multimer/deletion_perturb_out/AA_monomer_output.csv`

- `scp /path/to/deletion_perturb_out/AA_multimer_output.csv /path/to/local/Explainable-AlphaFold-Multimer/deletion_perturb_out/AA_multimer_output.csv`

## Copying predicted PDB structures to local directory
We also need to copy the predicted PDB files generated on Grace in your `/grace/path/to/garbage_out` to local. The best way to do this is to first copy the PDB files we will need to a subdirectory of garbage_out on Grace, and then copy only these PDB files to your local computer. This can be done as follows:

For monomer PDB files:
- `cd /grace/path/to/garbage_out/monomer_garbage_out`
- `cp **/*unrelaxed_rank_001*.pdb ../monomer_all_pdb`
  
then in another terminal:

- `scp -r /grace/path/to/garbage_out/monomer_garbage_out/monomer_all_pdb /path/to/local/Explainable-AlphaFold-Multimer/garbage_out/monomer_garbage_out/monomer_all_pdb`

For multimer PDB files:
- `cd /grace/path/to/garbage_out/multimer_garbage_out`
- `cp **/*unrelaxed_rank_001*.pdb ../multimer_all_pdb`
  
then in another terminal:

- `scp -r /grace/path/to/garbage_out/multimer_garbage_out/multimer_all_pdb /path/to/local/Explainable-AlphaFold-Multimer/garbage_out/multimer_garbage_out/multimer_all_pdb`

For antibody/antigen monomer PDB files:
- `cd /grace/path/to/garbage_out/AA_monomer_garbage_out`
- `cp **/*unrelaxed_rank_001*.pdb ../AA_monomer_all_pdb`
  
then in another terminal:

- `scp -r /grace/path/to/garbage_out/AA_monomer_garbage_out/AA_monomer_all_pdb /path/to/local/Explainable-AlphaFold-Multimer/garbage_out/AA_monomer_garbage_out/AA_monomer_all_pdb`

For antibody-antigen multimer PDB files:
- `cd /grace/path/to/garbage_out/AA_multimer_garbage_out`
- `cp **/*unrelaxed_rank_001*.pdb ../AA_multimer_all_pdb`
  
then in another terminal:

- `scp -r /grace/path/to/garbage_out/AA_multimer_garbage_out/AA_multimer_all_pdb /path/to/local/Explainable-AlphaFold-Multimer/garbage_out/AA_multimer_garbage_out/AA_multimer_all_pdb`

## Copying ID csv files for monomers
We also use the AlphaFold job ID for monomers later in data processing, so we need these files as well. Execute the following commands:

For generic monomer csv files:
- `cd /grace/path/to/garbage_out/monomer_garbage_out`
- `cp **/*.csv ../monomer_all_csv`

For antibody/antigen monomer csv files:
- `cd /grace/path/to/garbage_out/AA_monomer_garbage_out`
- `cp **/*.csv ../AA_monomer_all_csv`

Mirdita, M., Schütze, K., Moriwaki, Y. et al. ColabFold: making protein folding accessible to all. Nat Methods 19, 679–682 (2022). https://doi.org/10.1038/s41592-022-01488-1
