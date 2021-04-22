# Host-pathogen interaction using machine learning on microarray fluorescence data

This repository contains the scripts used in the following paper:
"Mucin-mimetic glycan arrays integrating machine learning for analyzing receptor pattern recognition by influenza A viruses", Cell Chem. (Submitted)
Preprint available at: https://www.biorxiv.org/content/10.1101/2021.04.17.440161v1

In this work, we show how Influenza A Viruses (IAVs) evolve to infect human hosts. IAVs gain access to host cells by recognizing the presentation of glycan receptors on the cellular glycocalyx surfaces. Using synthetic mimetics of glycoproteins that model the glyocalyx receptor presentation, we created data sets for viral binding fluorescence intensities for avian as well as human receptors. Similarities and differences between the binding preferences in these two data sets, which is impossible to conclude using chemical intuition, was revealed by Support Vector Machine (SVM)-based machine learning algorithm. The workflow for this pipeline is shown below

<p align="center">
    <img src="https://github.com/SingharoyLab/H1N1_host_interaction/blob/master/Workflow.jpeg" width="668" height="501">
</p>

## Pre-requisites

All scripts are written in python3, using jupyter notebook. The scripts will run with any standard jupyter notebook implementation with python3. For information on jupyter notebook, 
see: https://jupyter.org/

We recommend installing jupyter notebook through the anaconda platform
* https://www.anaconda.com/
* https://docs.anaconda.com/ae-notebooks/user-guide/basic-tasks/apps/jupyter/

## Selecting the cutoff

Data reading is done by the _read.py script in the glycan class. The target column in the raw data ("Mean Viral Fluorescence") is a continuous data that reports the intensity of viral binding fluorescence. For our purpose, this data needs to be converted into categorical ("binder"/"non-binder") format. To do this, we make use of the fact that the virus is a non-binder to lactose. By looking at the fluorescence intensity distributions from the three glycan types (2,3-SiaLac, 2-6-SiaLac, and Lactose), we identify the cutoff to be the lowest normalized mean viral fluorescence for which the lactose fluorescence intensity is ~0. The scripts 01_selecting_cutoff_egg.ipynb and 02_selecting_cutoff_mdck.ipynb do this for the H1N1 EGG (avian) and H1N1 MDCK (human) virus data sets, respectively.
    
## Data preparation and optimizing SVM learning

Next, we prepare the data for SVM learning. For this, we first scale every numerical, continuous variable to a range of [0,1] to avoid bias from higher values. Categorical features like glycan typue was transformed to numeric by mapping to a 2D space where each glycan type was represented either by (1,0) or (0,1). Scripts to do this are included in the glycan class (_prepare.py). This data set was then split into a training set and a test set. Testing set contained 33% of the data, which can be controlled by the "test_size" parameter of the getTrainTest function of the glycan class. 

Number of iterations of SVM learning was incrementally varied, and model performance was evaluated with accuracy, precision, recall, and F-1 score. The scripts 03_egg_convergence.ipynb and 04_MDCK_convergence.ipynb do this for the H1N1 EGG and H1N1 MDCK virus data sets, respectively. 05_plot_performance.ipynb creates the plot for these performance evaluations, that has been used in the supporting information of the paper (Fig. S17).

## Evaluating model performance

Performance of the optimized model was then evaluated in terms of a confusion matrix, where the diagonal elements show the numbers of correct predictions (true positives and true negatives respectively), and the off-diagonal elements show the the numbers of incorrect predictions (false positives and false negatives respectively). 06_SVM_egg.ipynb and 07_SVM_mdck.ipynb does this for the H1N1 EGG and H1N1 MDCK virus data sets, respectively.

## Learning the "rules of binding"

Comparison between avian and human receptors was performed by comparing results of "self-model" and "cross-model" on H1N1 MDCK virus data, wherein "self-model" is the model trained on H1N1 MDCK virus data, and "cross-model" is the model trained on H1N1 EGG data. The script 08_compare_self_and_cross.ipynb performs this task. Comments are provided within the script to describe the steps of this analysis. The flowchart for this analysis is shown below

<p align="center">
    <img src="https://github.com/SingharoyLab/H1N1_host_interaction/blob/master/Flowchart.jpeg" width="668" height="501">
</p>

 
