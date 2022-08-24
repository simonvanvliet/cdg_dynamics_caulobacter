#!/bin/bash

#SBATCH --job-name=Delta2_Batch
#SBATCH --time=6:00:00
#SBATCH --qos=6hours    
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --partition=a100  #a100 or rtx8000
#SBATCH --gres=gpu:1        

# Paths to STDOUT or STDERR files should be absolute or relative to current working directory
#SBATCH --output=delta_batch_log-%J.oe             #This is the joined STDOUT and STDERR file
#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user=simon.vanvliet@unibas.ch        #You will be notified via email when your task ends or fails

#This job runs from the current working directory

ml Java/11.0.3_7
ml FFmpeg

#load your required modules below
#################################
eval "$(conda shell.bash hook)"
conda activate delta2_env
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/"

#export your required environment variables below
#################################################

#add your command lines below
#############################
python -u delta_batch_process_Cc_s2.py > delta_python_log-%J.out 
#python -u delta_batch_process_PA.py > delta_python_log-%J.out 