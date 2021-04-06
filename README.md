# Wettability_Metal-IonocovalentCeramic

This repository provides two main components:

- Metal-ionocovalent ceramic wettability dataset.
- Python code for predicting the wettability of arbitrary metal-ionocovalent ceramic pairs.

The following paper describes the details of the machine learning model developed to predict the metal-ionocovalent ceramic wettability: [Machine Learning of Metal-Ceramic Wettability](https://doi.org/10.1016/j.jmat.2021.03.014)

## Table of Contents

- [Usage](#usage)
  - [Define a customized dataset](#define-a-customized-dataset)
  - [Train a CGCNN model](#train-a-cgcnn-model)
  - [Predict material properties with a pre-trained CGCNN model](#predict-material-properties-with-a-pre-trained-cgcnn-model)
- [How to cite](#how-to-cite)


## Usage

If you are new to Python, the easiest way of using the WettingAngleEstimator is via [Google Colab Notebook](https://colab.research.google.com/drive/1lrOwH4iu7_jRMpPh8X1SnAMJn5eJCD8V?usp=sharing).

1. Save a copy of the aforementioned Google Colab Notebook by using File > Save a copy in Drive.
2. Run the first cell by using Ctrl + Enter.
3. If you would like to use the interactive mode, where the code asks for user inputs, run the cell in the interactive mode section.
4. If you would like to use the type-in mode, where you can type in the information about the metal-ceramic pairs and temperature of interest before running the code, enter the necessary information following the instructions in the first cell of the type-in mode section and run the cells therein.

If you are experienced in Python, feel free to use either .ipynb or .py file in whatever way is convenient for you.

### Define metal-ceramic pairs of interest 

The current version allows three different ways of specifying the metal-ceramic pairs of interest.
1. One metal-ceramic pair (e.g., Fe and Si1O2)
2. One metal and a list of ceramics (e.g., Li and Li-ion/electron insulator (LEI) candidates): `lists_Li-LEIcandidatess.csv` is an exemplary .csv file.
3. One metal and a list of ceramics retrieved from Inorganic Crystal Structure Database (e.g., Al and all the oxides with a bandgap greater 2.5 eV in the ICSD database)

### Define a temperature range of interest 

Define the lowest temperature, the highest temperature, and the temperature interval of interest.

### Define a wetting angle range of interest

If you would like to collect only the results for the pairs of which predicted wetting angles are in a certain range, specify a wetting angle range of interest.
