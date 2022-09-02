#!/bin/bash

#SBATCH --job-name=Delta2_BatchPa
#SBATCH --time=6:00:00
#SBATCH --qos=6hours    
#SBATCH --cpus-per-task=4
#SBATCH --mem=256G
#SBATCH --partition=rtx8000,a100
#SBATCH --gres=gpu:1        

# Paths to STDOUT or STDERR files should be absolute or relative to current working directory
#SBATCH --output=delta_batch_log-%J.oe             #This is the joined STDOUT and STDERR file
#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user=simon.vanvliet@unibas.ch        #You will be notified via email when your task ends or fails

#This job runs from the current working directory

#load your required modules below
#################################
ml Java/11.0.3_7
ml FFmpeg

eval "$(conda shell.bash hook)"
conda activate delta2_env
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/"

#add your command lines below
#############################
#-u forces stdout to print directly
python -u delta_batch_process_Pa_Twitch.py
echo Finished

# LOGFILE=delta_python_log-CcFast-${SLURM_JOB_ID}.oe 
# ERRFILE=delta_python_err-CcFast-${SLURM_JOB_ID}.oe 
# python -u delta_batch_process_Cc_s2_fast.py 2>$ERRFILE  1>$LOGFILE 