# Explainable-AlphaFold-Multimer
Repository supplementing the CPSC 471 final project on the explainability of AlphaFold-Multimer

# Detailed instructions on running code

## Setting up local directories
Copy the entire file structure on Github to your local computer.

## Generating configuration files:
Run the notebooks `create_configs.ipynb` and `create_AA_configs.ipynb` in Explainable-AlphaFold-Multimer/data_processing. This will generate configuration files in Explainable-AlphaFold-Multimer/config_files which will be used to run AlphaFold and AlphaFold-Multimer on Grace.

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

- `scp /grace/path/to/deletion_perturb_out/monomer_output.csv /path/to/local/deletion_perturb_out/monomer_output.csv`

- `scp /grace/path/to/deletion_perturb_out/multimer_output.csv /path/to/local/deletion_perturb_out/multimer_output.csv`

- `scp /path/to/deletion_perturb_out/AA_monomer_output.csv /path/to/local/deletion_perturb_out/AA_monomer_output.csv`

- `scp /path/to/deletion_perturb_out/AA_multimer_output.csv /path/to/local/deletion_perturb_out/AA_multimer_output.csv`

## Copying predicted PDB structures to local directory
We also need to copy the predicted PDB files generated on Grace in your `/grace/path/to/garbage_out` to local. The best way to do this is to first copy the PDB files we will need to a subdirectory of garbage_out on Grace, and then copy only these PDB files to your local computer. This can be done as follows:

For monomer PDB files:
- `cd /grace/path/to/garbage_out/monomer_garbage_out`
- `cp **/*unrelaxed_rank_001*.pdb ../monomer_all_pdb`
  
then in another terminal:

- `scp -r /grace/path/to/garbage_out/monomer_garbage_out/monomer_all_pdb /path/to/local/garbage_out/monomer_garbage_out`

For multimer PDB files:
- `cd /grace/path/to/garbage_out/multimer_garbage_out`
- `cp **/*unrelaxed_rank_001*.pdb ../multimer_all_pdb`
  
then in another terminal:

- `scp -r /grace/path/to/garbage_out/multimer_garbage_out/multimer_all_pdb /path/to/local/garbage_out/multimer_garbage_out`

For antibody/antigen monomer PDB files:
- `cd /grace/path/to/garbage_out/AA_monomer_garbage_out`
- `cp **/*unrelaxed_rank_001*.pdb ../AA_monomer_all_pdb`
  
then in another terminal:

- `scp -r /grace/path/to/garbage_out/AA_monomer_garbage_out/AA_monomer_all_pdb /path/to/local/garbage_out/AA_monomer_garbage_out`

For antibody-antigen multimer PDB files:
- `cd /grace/path/to/garbage_out/AA_multimer_garbage_out`
- `cp **/*unrelaxed_rank_001*.pdb ../AA_multimer_all_pdb`
  
then in another terminal:

- `scp -r /grace/path/to/garbage_out/AA_multimer_garbage_out/AA_multimer_all_pdb /path/to/local/garbage_out/AA_multimer_garbage_out`

## Copying ID csv files for monomers
We also use the AlphaFold job ID for monomers later in data processing, so we need these files as well. Execute the following commands:

For generic monomer csv files:
- `cd /grace/path/to/garbage_out/monomer_garbage_out`
- `cp **/*.csv ../monomer_all_csv`

then in another terminal:

- `scp -r /grace/path/to/garbage_out/monomer_garbage_out/monomer_all_csv /path/to/local/garbage_out/monomer_garbage_out`

For antibody/antigen monomer csv files:
- `cd /grace/path/to/garbage_out/AA_monomer_garbage_out`
- `cp **/*.csv ../AA_monomer_all_csv`

then in another terminal:

- `scp -r /grace/path/to/garbage_out/monomer_garbage_out/AA_monomer_all_csv /path/to/local/garbage_out/AA_monomer_garbage_out`

## Checking for failed runs and rerunning if necessary
Note: you can now exit Grace. The rest of the instructions are meant to be followed locally (unless a rerun of AlphaFold is necessary; see this section)

The next step is to check if any AlphaFold or AlphaFold-Multimer runs failed. Run the notebooks `monomer_retry_failed_jobs.ipynb` and `multimer_retry_failed_jobs.ipynb` (in /path/to/local/data_processing) to check if any of the runs for generic monomers and multimers, respectively, have failed. If the "missing_df" is empty, all runs were successful; save the "matching_df" to a csv file by uncommenting the corresponding line in each notebook and running the code block.

To check if any antibody-antigen runs failed, run the notebook `AA_retry_failed_jobs.ipynb` in /path/to/local/Explainable-AlphaFold-Multimer/data_processing. Make sure to save the "matching_df" to csv when there are no missing runs.

If any of the runs failed (the "missing_df" is non-empty), you must rerun AlphaFold and AlphaFold multimer on Grace using a new configuration file. If this is the case, then in the "Save missing data asa 'to fill in' config file" section in the `retry_failed_jobs` notebook, uncomment the line that saves "fill_df" to csv and run the code block. There will be a new configuration file in /path/to/local/config_files; copy this file to Grace in /grace/path/to/config_files. Then, in the corresponding slurm script on Grace (in /grace/path/to/slurm_scripts), uncomment the line that sets the original configuration file, and uncomment the line that sets the configuration to the "fill" configuration file. Also ensure that the `#SBATCH --array=1-<NJOBS>` argument has the correct value for <NJOBS>: it should be the last number in the ArrayTaskID column of the fill configuration file.

## Processing the completed AlphaFold / AlphaFold-Multimer outputs
Once all runs are successful, you should have four files in /path/to/local/matching_deletion_perturb_out:

1. matching_monomer_output.csv
2. matching_multimer_output.csv
3. matching_AA_monomer_output.csv
4. matching_AA_multimer_output.csv

Run the two following notebooks in /path/to/local/data_processing to process these output csv files in preparation for PyMOL visualizations:

- `prepare_for_pymol.ipynb`
- `AA_prepare_for_pymol.ipynb`

There should now be some PDB files in the subdirectories of /path/to/local/selected_pdb_files. Additionally, there should be four new files in /path/to/local/Explainable-AlphaFold-Multimer/processed_deletion_perturb_out:

1. processed_monomer_output.csv
2. processed_multimer_output.csv
3. processed_AA_monomer_output.csv
4. processed_AA_multimer_output.csv

## Generate PyMOL scripts (.pml files)
We are now ready to generate the scripts to be run by PyMOL for protein complex visualization. In /path/to/local/data_processing/, run `write_all_pymol_scripts.ipynb`. You should then see the subdirectories of /path/to/local/pymol populate with .pml files. In each of these directories (each of which corresponds to multimers or monomers, of the generic or antigen-antibody variety) contains PyMOL scripts, organized into a set of subdirectories: pTM, ipTM, and pLDDT. Each of these subdirectories corresponds to a different score produced by AlphaFold. The PyMOL scripts in a given directory, when ran, will color each protein complex according to the given delta score.

## Visualizing protein complexes with PyMOL
Apply for a student license from PyMOL at https://pymol.org/edu/. Download the PyMOL GUI, and perform the following steps:

1. Open PyMOL
2. Go to File > Run Script
3. Select the PML file corresponding to the protein complex and score you wish to visualize, and click open.
4. To align objects (e.g. a multimer and one of its mononumeric chains), you can type the following command into the PyMOL GUI command line:

- align object1, object2

Multimers and monomers are named according to their complex IDs and the delta score by which they are being colored. So, for example, we would align the 8be1_A_8be1_B multimer with its "A" chain (8be1_A) when we are coloring it by (mean) LDDT with the command:

- align 8be1_A_8be1_B_delta_mean_pLDDT, 8be1_A_delta_mean_pLDDT

To produce a png image of whatever is displayed on the screen, with a transparent background, execute the following command:

- png /path/to/local/pymol/<plots_directory>/<name_of_png>.png, 0, 0, -1, ray=1

Note that <plots_directory>, for organizational purposes, should refer to the type of visualization you were trying to represent with the png. For example, if you were comparing pLDDT for multimers vs. mononomers, you might choose to put the png image in /path/to/local/pymol/plots_pLDDT_vs_pLDDT.

## Generating analysis plots

## References

Mirdita, M., Schütze, K., Moriwaki, Y. et al. ColabFold: making protein folding accessible to all. Nat Methods 19, 679–682 (2022). https://doi.org/10.1038/s41592-022-01488-1

PyMOL. The PyMOL Molecular Graphics System, Version 3.0 Schrödinger, LLC.

Wensi Zhu, Aditi Shenoy, Petras Kundrotas, Arne Elofsson, Evaluation of AlphaFold-Multimer prediction on multi-chain protein complexes, Bioinformatics, Volume 39, Issue 7, July 2023, btad424, https://doi.org/10.1093/bioinformatics/btad424

Yin Rui and Brian G. Pierce, "Evaluation of AlphaFold Antibody-Antigen Modeling with Implications for Improving Predictive Accuracy" https://doi.org/10.1101/2023.07.05.547832
