# Metal-Ionocovalent Ceramic Wettability

This repository provides two main components:

- Metal-ionocovalent ceramic wettability dataset.
- Python code for predicting the wettability of arbitrary metal-ionocovalent ceramic pairs.

The following paper describes the details of the machine learning model developed to predict the metal-ionocovalent ceramic wettability: [Machine Learning of Metal-Ceramic Wettability](https://doi.org/10.1016/j.jmat.2021.03.014)



## Usage

If you are new to Python, the easiest way of using the WettingAngleEstimator is via [Google Colab Notebook](https://colab.research.google.com/drive/1lrOwH4iu7_jRMpPh8X1SnAMJn5eJCD8V?usp=sharing).

1. Save a copy of the Google Colab Notebook by using "File > Save a copy in Drive".
2. Execute the first cell; to execute a cell, hover the mouse over [ ] and press the play button to the upper left (or just press shift-enter). It may take a few minutes to be completed.
3. The current version provides two different ways of specifying the systems of interest; the interactive mode and the type-in mode.
  3-1. Interactive mode
  This mode asks for the necessary information during operation. Execute the cell and answer the questions that appear.
  3-2. Type-in mode
  This mode requires the user to enter the necessary information before executing the cell. Follow the instructions written in the cell. After entering all the information execute the first cell and the second cell sequentially.

If you are experienced in Python, feel free to use either .ipynb or .py file in whatever way is convenient for you.

### - Define metal-ceramic pairs of interest 

The current version allows three different ways of specifying the metal-ceramic pairs of interest.
1. One metal-ceramic pair (e.g., Fe and Si1O2)
2. One metal and a list of ceramics (e.g., Li and Li-ion/electron insulator (LEI) candidates): `prediction/lists_Li-LEIcandidates.csv` is an exemplary .csv file.
3. One metal and a list of ceramics retrieved from Inorganic Crystal Structure Database (e.g., Al and all the oxides in the ICSD catalog that have a bandgap greater 2.5 eV)

### - Define a temperature range of interest 

Define the lowest temperature, the highest temperature, and the temperature interval of interest.

### - Define a wetting angle range of interest

Specify a wetting angle range of interest if you would like to collect only the results for the pairs of which predicted wetting angles are in a certain range,



## How to cite

If you use this code or data in your research, please consider citing the following work:

So Yeon Kim, Ju Li. *Machine Learning of Metal-Ceramic Wettability.* Journal of Materiomics, 2021. [DOI:10.1016/j.jmat.2021.03.014](https://doi.org/10.1016/j.jmat.2021.03.014)

```
@article{KIM2021,
title = {Machine Learning of Metal-Ceramic Wettability},
journal = {Journal of Materiomics},
year = {2021},
issn = {2352-8478},
doi = {https://doi.org/10.1016/j.jmat.2021.03.014},
url = {https://www.sciencedirect.com/science/article/pii/S2352847821000629},
author = {So Yeon Kim and Ju Li},
keywords = {Metal-ceramic wettability, Wetting angle, Machine learning, High-throughput screening, Solid-state batteries},
}
```
