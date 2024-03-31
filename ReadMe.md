# ReadMe

This repository contains the code used for analyzing the single-cell microscopy data described in the following publication:

A genetically encoded biosensor to monitor dynamic changes of c-di-GMP with high temporal resolution

Andreas Kaczmarczyk, Simon van Vliet, Roman Peter Jakob, Raphael Dias Teixeira, Inga Scheidat, Alberto Reinders, Alexander Klotz, Timm Maier, Urs Jenal

Biozentrum, University of Basel, 4056 Basel, Switzerland

Correspondence to: urs.jenal[at]unibas.ch, andreas.kaczmarczyk[at]unibas.ch

Code developed by:

Simon van Vliet  

Biozentrum, University Basel  

simon.vanvliet[at]unibas.ch

## Requirements

- create a conda environment using the specified `environment.yml` file

## Contents

### Jupyter Notebooks

Jupyter notebooks are provided to recreate the data analysis. Most notebooks have three versions, one for Caulobacter (`_Cc`) and Pseudomonas (`Pa`) at low time resolution and one for  Caulobacter (`_Cc_Fast`) at high time resolution.

To replicate the results follow the following steps:

1. Run the `1_filter_data_[Cc/Pa/Cc_Fast]` notebooks to filter out tracklets with tracking / segmentation errors
2. Run the `2_plot_data_[Cc/Pa/Cc_Fast]` notebooks to recreate the main figures
3. Run the `3_plot_lineage_trees]` notebooks to recreate the lineage tree figures

### Additional Code

- `filter_tracks.py`: function definition for tracklet filtering to identify segmentation/tracking results, used in `1_filter_data_Cc_Fast` notebook
- `filter_paired_tracks.py`: function definition for paired tracklet filtering to identify segmentation/tracking results, used in `1_filter_data_[Cc/Pa]` notebooks
- `plot_lineage_tree.py`: class definition of function used to plot lineage trees

### Data Files

The data_files folder contains data frames of the filtered cell lineages.

## Notes

Time-lapse movies were analyzed using [DeLTA 2.0](https://delta.readthedocs.io/en/latest/). The output of DeLTA was processed using the `delta_postprocess.py` code that converts the DeLTA lineage object into Pandas dataframes with lineages separated into separate tracks. The Notebooks `0_postprocess_delta_[Cc/Pa/Cc_Fast]` used for this are provided as reference.
