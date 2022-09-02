#!/bin/bash
#SBATCH --job-name=convert
#SBATCH --time=0:30:00
#SBATCH --qos=30min    
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G

# Paths to STDOUT or STDERR files should be absolute or relative to current working directory
#SBATCH --output=delta_batch_log-%J.oe             #This is the joined STDOUT and STDERR file
#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user=simon.vanvliet@unibas.ch        #You will be notified via email when your task ends or fails

#This job runs from the current working directory

#load your required modules below
#################################
eval "$(conda shell.bash hook)"
conda activate delta2_env
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib/"

#add your command lines below
#############################
#-u forces stdout to print directly
python -u convert_data.py 
echo Finished

