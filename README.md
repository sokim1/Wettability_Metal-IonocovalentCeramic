# Metal-Ionocovalent Ceramic Wettability

This repository provides two main components:

- Metal-ionocovalent ceramic wettability dataset.
- WettingAnglePredictor (WAP): Python code for predicting the wettability of arbitrary metal-ionocovalent ceramic pairs.

*Note: Most of the wetting angles listed in the dataset are measured via the conventional sessile drop method and thus are close to advancing contact angles rather than receding or equilibrium contact angles, which require the application of controlled vibrations for the measurement. Accordingly, the predicted wetting angles are also expected to be close to advancing contact angles.*

The following paper describes the details of the machine learning model developed to predict the metal-ionocovalent ceramic wettability: So Yeon Kim and Ju Li, "[Machine Learning of Metal-Ceramic Wettability](https://doi.org/10.1016/j.jmat.2021.03.014)", Journal of Materiomics (2021).




## Workflow of the WettingAnglePredictor

#### 1. Define metal-ionocovalent ceramic pairs of interest 

The current version can handle three different cases:
- One metal-one ceramic pair (e.g., Fe and Si1O2)
- One metal and a list of ceramics (e.g., Li and Li-ion/electron insulator (LEI) candidates): A user needs to provide a CSV file with the list of ceramics. `prediction/lists_Li-LEIcandidates.csv` is an exemplary .csv file.
- One metal and a list of ceramics retrieved from Inorganic Crystal Structure Database (e.g., Al and all the oxides in the ICSD catalog that have a bandgap between 2 and 3 eV): A user needs to write a MATCHBOOK, which is material keywords with arguments. For example, to retrieve all the oxides in the ICSD catalog that have a bandgap between 2 and 3 eV, "species((O)), Egap(2*,*3),catalog(icsd)" should be entered. The way of writing it is explained in Figure 1 and Appendix C of this [article](https://doi.org/10.1016/j.commatsci.2017.04.036).

*Note: The prediction accuracy for the material pairs other than metal-ionocovalent ceramic pairs could be much lower.*

#### 2. Specify the temperature range of interest 

Specify the minimum temperature, the maximum temperature, and the temperature interval of interest. For example, if you are interested in wetting angles at 1800 K, 1900 K, and 2000 K, you need to enter "1800-2000-100". 

#### 3. Specify the wetting angle range of interest

Specify the wetting angle range of interest. For example, if you are interested only in metal-ionocovalent ceramic pairs of which wetting angles are expected to be below 90 degree, you need to enter "-90". Other examples are as follows: "50-", "0-90", "all", etc.




## How to run the WettingAnglePredictor

#### If you are new to Python, 
the easiest way of using the WettingAnglePredictor is via Google Colab Notebook.

1. Save a copy of the [Google Colab Notebook](https://colab.research.google.com/drive/18aNeQ__aDx4gdNn-y7q1OJwmgm1dNyyW?usp=sharing) by using "File > Save a copy in Drive".
2. Execute the first cell; to execute a cell, hover the mouse over a square bracket([ ]) on the upper left of the cell and press the play button that appears (or just press Shift- + Enter). It may take a few minutes to be completed.
3. The current version provides two different ways of specifying the systems of interest; the interactive mode and the type-in mode. Each mode can be found below the first cell.
    - Interactive mode asks for the necessary information during operation. Execute the cell and answer the questions that appear.
    - Type-in mode requires a user to enter the necessary information before executing the cell. Follow the instructions written in the cell. After entering all the information, execute the first cell and the second cell sequentially.
4. Find the CSV file with the results in the session storage by clicking the folder icon on the left sidebar.

#### If you prefer using the Jupyter Notebook, 
one easy way of installing prerequisites is via [conda](https://conda.io/docs/index.html).

1. Install [conda](http://conda.pydata.org/).
2. Run the following command to create a new [environment](https://conda.io/docs/user-guide/tasks/manage-environments.html) named `wap` and activate the environment. 

```bash
conda upgrade conda
conda create --name wap
conda activate wap
```

3. Install all the prerequisites by running:

```bash
conda install -c conda-forge pymatgen==2020.12.31
pip install matminer
conda install pywin32
pip install jupyter notebook
```

4. Open the Jupyter Notebook and run the WettingAnglePredictor.

#### If you are experienced in Python, 
feel free to use the codes provided in the `prediction/WettingAnglePredictor_v1.ipynb` file in whatever way is convenient for you.




## How to contribute

The prediction accuracy could be improved by increasing the number of data points used to train the machine learning model. We would appreciate it if you could please let us know using this [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSexDIOBS0Tbve2uUbCfaiWBIl0O0ttWUuunHcxtojoptjEaEQ/viewform?usp=sf_link) in case you find experimental results that are not in `dataset/database.csv` from literature or publish new experimental results by yourself. The database will be updated monthly and the name/affiliation of contributors will be listed in `dataset/database-contributors.csv`.




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
