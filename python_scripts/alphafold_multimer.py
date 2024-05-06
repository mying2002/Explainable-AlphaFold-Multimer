# import required packages
import sys
import os
import re
import hashlib
# import random
import csv

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from Bio import BiopythonDeprecationWarning
warnings.simplefilter(action='ignore', category=BiopythonDeprecationWarning)
from pathlib import Path
from colabfold.download import download_alphafold_params, default_data_dir
from colabfold.utils import setup_logging
from colabfold.batch import get_queries, run, set_model_type
from colabfold.plot import plot_msa_v2

import os
# import numpy as np

from colabfold.colabfold import plot_protein
from pathlib import Path
import matplotlib.pyplot as plt


# processes command line inputs (ie. deletes amino acid from one seq)
# requires 4 inputs: seq1 seq2 which_seq delete_index
def process_command_line_args(seq1, seq2, which_seq, delete_index):
    # process command line arguments
    if which_seq == 1:
        if delete_index not in range(len(seq1)):
            print("Invalid which_seq and delete_index combination")
            sys.exit(1)

        seq1 = seq1[0:delete_index] + seq1[(1+delete_index):]

    elif which_seq == 2:
        if delete_index not in range(len(seq2)):
            print("Invalid which_seq and delete_index combination")
            sys.exit(1)

        seq2 = seq2[0:delete_index] + seq2[(1+delete_index):]

    elif which_seq == 0 and delete_index == -1:
        pass

    else:
        print("Invalid which_seq and delete_index combination")
        sys.exit(1)

    return [seq1, seq2]

# add hash to the name of the test
def add_hash(x,y):
  return x+"_"+hashlib.sha1(y.encode()).hexdigest()[:5]

def main():
    """
            --------------------------- STEP 0: grab command line arguments ---------------------------
    """
    # check usage is correct
    if len(sys.argv) != 7: # includes script name
        print("Usage: python script.py seq1_id seq2_id seq1 seq2 which_seq delete_index")
        sys.exit(1)

    # grab command line arguments
    seq1_id = sys.argv[1]
    seq2_id = sys.argv[2]
    og_seq1 = sys.argv[3] # original sequence
    og_seq2 = sys.argv[4] # original sequence
    which_seq = int(sys.argv[5])
    delete_index = int(sys.argv[6])
    seq1, seq2 = process_command_line_args(og_seq1, og_seq2, which_seq, delete_index)

    """
            ----------------------------- STEP 1: set up inputs and job --------------------------------
    """
    query_sequence = seq1 + ':' + seq2
    # jobname = seq1_id + "_" + seq2_id # just protein sequence metadata
    jobname = seq1_id + "_" + seq2_id + "_" + str(which_seq) + "_" + str(delete_index) # all metadata; careful since will create lots of files
    num_relax = 0 # ! keep at 0
    template_mode = "none"
    use_amber = num_relax > 0 # ! don't use amber

    # remove whitespaces
    query_sequence = "".join(query_sequence.split())

    basejobname = "".join(jobname.split())
    basejobname = re.sub(r'\W+', '', basejobname)
    jobname = add_hash(basejobname, query_sequence)

    # check if directory with jobname exists
    def check(folder):
        if os.path.exists(folder):
            return False
        else:
            return True
    if not check(jobname): # ! increments counter to make a new folder each time
        n = 0
        while not check(f"{jobname}_{n}"): n += 1
        jobname = f"{jobname}_{n}"

    # make directory to save results
    os.makedirs(jobname, exist_ok=True)

    # save queries
    queries_path = os.path.join(jobname, f"{jobname}.csv")
    with open(queries_path, "w") as text_file:
        text_file.write(f"id,sequence\n{jobname},{query_sequence}")

    # ! don't use templates
    custom_template_path = None
    use_templates = False

    print("jobname",jobname)
    print("sequence",query_sequence)
    print("length",len(query_sequence.replace(":","")))

    """
            ------------------------ STEP 2: specify settings for alphafold -----------------------------
    """
    # block 1: model specs
    msa_mode = "mmseqs2_uniref_env" # hardcoded
    pair_mode = "unpaired_paired"
    # ! assumes msa_mode = "mmseqs2_uniref_env"
    a3m_file = os.path.join(jobname,f"{jobname}.a3m")

    # block 2: advanced settings
    model_type = "auto" # ["auto", "alphafold2_ptm", "alphafold2_multimer_v1", "alphafold2_multimer_v2", "alphafold2_multimer_v3", "deepfold_v1"]
    num_recycles = "1" # ["auto", "0", "1", "3", "6", "12", "24", "48"]
    recycle_early_stop_tolerance = "auto" # ["auto", "0.0", "0.5", "1.0"]
    relax_max_iterations = 200 # [0, 200, 2000]
    pairing_strategy = "greedy" # ["greedy", "complete"]

    max_msa = "auto" # ["auto", "512:1024", "256:512", "64:128", "32:64", "16:32"]
    num_seeds = 1 # [1,2,4,8,16] {type:"raw"}
    use_dropout = False # {type:"boolean"}

    num_recycles = None if num_recycles == "auto" else int(num_recycles)
    recycle_early_stop_tolerance = None if recycle_early_stop_tolerance == "auto" else float(recycle_early_stop_tolerance)
    if max_msa == "auto": max_msa = None

    save_all = False
    save_recycles = False
    # save_to_google_drive = False
    dpi = 200

    """
            ------------------------------- STEP 3: run predictions -------------------------------
    """

    # ! does not display images

    # - not sure what this does - #
    # try:
    #     K80_chk = os.popen('nvidia-smi | grep "Tesla K80" | wc -l').read()
    # except:
    #     K80_chk = "0"
    #     pass
    # if "1" in K80_chk:
    #     print("WARNING: found GPU Tesla K80: limited to total length < 1000")
    #     if "TF_FORCE_UNIFIED_MEMORY" in os.environ:
    #         del os.environ["TF_FORCE_UNIFIED_MEMORY"]
    #     if "XLA_PYTHON_CLIENT_MEM_FRACTION" in os.environ:
    #         del os.environ["XLA_PYTHON_CLIENT_MEM_FRACTION"]

    result_dir = jobname 
    log_filename = os.path.join(jobname,"log.txt")
    setup_logging(Path(log_filename))

    queries, is_complex = get_queries(queries_path)
    model_type = set_model_type(is_complex, model_type)

    if "multimer" in model_type and max_msa is not None:
        use_cluster_profile = False
    else:
        use_cluster_profile = True

    # ! big! downloads weights
    download_alphafold_params(model_type, Path("..")) # was Path(".")

    # first pass to find baseline results of model
    model_results = run(
        queries=queries,
        result_dir=result_dir, # None doesn't work; may need to use trash dir
        use_templates=use_templates,
        custom_template_path=custom_template_path,
        num_relax=num_relax,
        msa_mode=msa_mode,
        model_type=model_type,
        num_models=3, # was 5
        num_recycles=num_recycles,
        relax_max_iterations=relax_max_iterations,
        recycle_early_stop_tolerance=recycle_early_stop_tolerance,
        num_seeds=num_seeds,
        use_dropout=use_dropout,
        model_order=[1,2,3], # was [1,2,3,4,5]
        is_complex=is_complex,
        data_dir=Path(".."), # was Path("."); path to params folder
        keep_existing_results=False,
        rank_by="auto",
        pair_mode=pair_mode,
        pairing_strategy=pairing_strategy,
        stop_at_score=float(100),
        prediction_callback=None, # prediction_callback
        dpi=dpi,
        zip_results=False,
        save_all=save_all,
        max_msa=max_msa,
        use_cluster_profile=use_cluster_profile,
        input_features_callback=None, # input_features_callback
        save_recycles=save_recycles,
        user_agent="colabfold/google-colab-main",
    )

    """
            ---------------------- STEP 4: process final results -----------------------------
    """

    # grabs best model's outputs
    # print(model_results)
    mean_pLDDT_score = model_results['metric'][0][0]['mean_plddt']
    pTM_score = model_results['metric'][0][0]['ptm']
    ipTM_score = model_results['metric'][0][0]['iptm']

    # results_zip = f"{jobname}.result.zip"
    # os.system(f"zip -r {results_zip} {jobname}") # zips file and saves; don't run if don't need!

    # print(queries)
    # print(f"mean_pLDDT_score = {mean_pLDDT_score}")
    # print(f"pTM_score = {pTM_score}")
    # print(f"ipTM_score = {ipTM_score}")

    # write results to csv file
    output_file = '../deletion_perturb_out/multimer_output.csv'
    file_exists = os.path.isfile(output_file) # check if output file exists

    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write a header row if the file was just created
        if not file_exists:
            writer.writerow(['seq1_id', 'seq2_id', 'seq1', 'seq2', 'which_seq', 'delete_index', 'mean_pLDDT_score', 'pTM_score', 'ipTM_score'])
        
        # Write the numbers as a new row in the CSV file
        writer.writerow([seq1_id, seq2_id, og_seq1, og_seq2, which_seq, delete_index, mean_pLDDT_score, pTM_score, ipTM_score])


if __name__ == "__main__":
    main()