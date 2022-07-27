# CDG-Sensor single cell analysis

Code used for analyzing the data described in the following publication:

Code developed by:

Simon van Vliet  
Biozentrum, University Basel  
simon.vanvliet@unibas.ch

## Requirements

- create a conda environment using the specified `environment.yml` file
- install Delta 2.0 and add it to your search path following [these instructions](https://delta.readthedocs.io/en/latest/usage/installation.html)

## Contents

### Jupyter Notebooks

Jupyter notebooks are provided to recreate the data analysis. Most notebooks have two versions, one for Caulobacter (`_Cc`) and one for Pseudomonas (`Pa`).

To replicate the results follow the following steps:

1. Run the `0_postprocess_delta_[Cc/Pa]` notebooks to postprocess Delta 2.0 output
2. Run the `1_filter_data_[Cc/Pa]` notebooks to filter for cell pairs without tracking errors
3. Run the `2_plot_data_[Cc/Pa]` notebooks to recreate the main figure files
4. Run the `3_plot_lineage_trees]` notebooks to recreate the lineage tree figures

### Additional Code

- `delta_postprocess.py`: helper functions to convert Delta lineage object into Panda date frame with lineages separated into separate tracks
- `plot_lineage_tree.py`: class definition of function used to plot lineage trees
