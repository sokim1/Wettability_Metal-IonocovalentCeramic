# Metal-Ionocovalent Ceramic Wettability

This repository provides two main components:

- Metal-ionocovalent ceramic wettability dataset.
- WettingAngleEstimator: Python code for predicting the wettability of arbitrary metal-ionocovalent ceramic pairs.

The following paper describes the details of the machine learning model developed to predict the metal-ionocovalent ceramic wettability: [Machine Learning of Metal-Ceramic Wettability](https://doi.org/10.1016/j.jmat.2021.03.014)



## Workflow of the WettingAngleEstimator

#### 1. Define metal-ionocovalent ceramic pairs of interest 

The current version can handle three different cases:
- One metal-one ceramic pair (e.g., Fe and Si1O2)
- One metal and a list of ceramics (e.g., Li and Li-ion/electron insulator (LEI) candidates): A user needs to provide .csv file with the list of ceramics. `prediction/lists_Li-LEIcandidates.csv` is an exemplary .csv file.
- One metal and a list of ceramics retrieved from Inorganic Crystal Structure Database (e.g., Al and all the oxides in the ICSD catalog that have a bandgap greater than 2.5 eV): A user needs to write a MATCHBOOK, which is material keywords with arguments. For example, to retrieve all the oxides in the ICSD catalog that have a bandgap greater than 2.5 eV, "species((O)), Egap(2.5*),catalog(icsd)" should be entered. The way of writing it is explained in the Figure 1 and the Appendix C of this [article](https://doi.org/10.1016/j.commatsci.2017.04.036).

*Note: The prediction accuracy for the material pairs other than metal-ionocovalent ceramic pairs could be much lower.*

#### 2. Define the temperature range of interest 

Define the lowest temperature, the temperature range, and the temperature interval of interest. For example, if you are interested in wetting angles at 1800 K, 1900 K, and 2000 K, you need to enter "1800", "200", and "100" for the lowest temperature, the temperature range, and the temperature interval of interest, respectively. 

#### 3. Define the wetting angle range of interest

Specify the wetting angle range of interest. For example, if you are interested only in metal-ionocovalent ceramic pairs of which wetting angles are expected to be below 90 degree, you need to enter "-90".



## How to run the WettingAngleEstimator

If you are new to Python, the easiest way of using the WettingAngleEstimator is via [Google Colab Notebook](https://colab.research.google.com/drive/1lrOwH4iu7_jRMpPh8X1SnAMJn5eJCD8V?usp=sharing).

1. Save a copy of the Google Colab Notebook by using "File > Save a copy in Drive".
2. Execute the first cell; to execute a cell, hover the mouse over [ ] and press the play button to the upper left (or just press shift-enter). It may take a few minutes to be completed.
3. The current version provides two different ways of specifying the systems of interest; the interactive mode and the type-in mode. Each mode can be found below the first cell.
    - Interactive mode asks for the necessary information during operation. Execute the cell and answer the questions that appear.
    - Type-in mode requires a user to enter the necessary information before executing the cell. Follow the instructions written in the cell. After entering all the information, execute the first cell and the second cell sequentially.
4. Find your results by clicking the folder icon on the left sidebar.

If you are experienced in Python, feel free to use either .ipynb or .py file in whatever way is convenient for you.



## How to contribute

The prediction accuracy could be improved by increasing the number of datapoints used to train the machine learning model. We would appreciate it if you could please let us know using this [Google Form]() in case you find experimental results that are not in `dataset/database.csv` from literature or publish new experimental results by yourself. The database will be updated monthly and the name/affiliation of contributors will be listed in `dataset/database-contributors.csv`.



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
