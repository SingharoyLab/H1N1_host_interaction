# Host-pathogen interaction using machine learning on microarray fluorescence data

This repository contains the scripts used in the following paper:
"Mucin-mimetic glycan arrays integrating machine learning for analyzing receptor pattern recognition by influenza A viruses", Cell Chem. (Submitted)
Preprint available at: https://www.biorxiv.org/content/10.1101/2021.04.17.440161v1

In this work, we show how Influenza A Viruses (IAVs) evolve to infect human hosts. IAVs gain access to host cells by recognizing the presentation of glycan receptors on the cellular glycocalyx surfaces. Using synthetic mimetics of glycoproteins that model the glyocalyx receptor presentation, we created data sets for viral binding fluorescence intensities for avian as well as human receptors. Similarities and differences between the binding preferences in these two data sets, which is impossible to conclude using chemical intuition, was revealed by Support Vector Machine (SVM)-based machine learning algorithm. The workflow for this pipeline is shown below

<img align="center" src="https://github.com/SingharoyLab/H1N1_host_interaction/blob/master/Workflow.jpeg" width="500" height="500">

## Pre-requisites

All scripts are written in python3, using jupyter notebook. The scripts will run with any standard jupyter notebook implementation with python3. For information on jupyter notebook, see 
https://jupyter.org/

We recommend installing jupyter notebook through the anaconda platform
https://www.anaconda.com/
https://docs.anaconda.com/ae-notebooks/user-guide/basic-tasks/apps/jupyter/

## Selecting the cutoff

The target column in the raw data ("Mean Viral Fluorescence") is a continuous data that reports the intensity of viral binding fluorescence. For our purpose, this data needs to be converted into categorical ("binder"/"non-binder") format. To do this, we make use of the fact that the virus is a non-binder to lactose. By looking at the fluorescence intensity distributions from the three glycan types (2,3-SiaLac, 2-6-SiaLac, and Lactose), we identify the cutoff to be the lowest normalized mean viral fluorescence for which the lactose fluorescence intensity is ~0. The scripts 01_selecting_cutoff_egg.ipynb and 02_selecting_cutoff_mdck.ipynb do this for the H1N1 EGG (avian) and H1N1 MDCK (human) virus data sets, respectively.
    
## Optimizing SVM learning

TBD

## Evaluating model performance

TBD

## TBD

TBD

## Comparing avian and human receptor results





`python run_ADK.py > run_ADK.log`
    
### Sub-subheading 1

* Item 1
TBD

   

### Pre-requisites

* TBD
 
