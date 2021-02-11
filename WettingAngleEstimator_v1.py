option = int(input('Enter type (1: one metal-ceramic pair; 2: metal-list of ceramics; 3: ICSD screening): '))
metal = str(input('Enter metal of interest (e.g., Fe): '))

if option == 1:
  # (1) one pair: Please modify 'Ceramic' (e.g., 'Al2O3')
  ceramic = str(input('Enter ceramic of interest (e.g., Si1O2): '))
  substrate = pd.DataFrame([ceramic])
else:
    if option == 2:
      # (2) list: Please modify 'filename.csv' and 'header for compound list'
      filename = str(input('Enter the name of the csv file with the list of ceramics (e.g., filename.csv): '))
      header = str(input('Enter the header of the list of ceramics (e.g., ceramic): '))
    else: 
        if option == 3:
          # (3) ICSD search: Please modify "species(...)". Please refer to https://doi.org/10.1016/j.commatsci.2017.04.036.
          MATCHBOOK = str(input('Enter the MATCHBOOK referring to https://doi.org/10.1016/j.commatsci.2017.04.036 (e.g., ) : species((O:F),!S),nspecies(2*,*8),catalog(icsd)'))
          # Retrieve compounds with O or F but no S, of which the number of species is between 2 and 8.
        else: print('Error: check if necessary inputs are all entered')

Tinterest = str(input('Are you interested in wetting angles at a range of temperatures? (yes or no)'))

if Tinterest == 'no':
  T0 = int(input('Enter temperature of interest in Kelvin (e.g., 1800): '))
else:
    T0 = int(input('Enter the lower limit of the temperature of interest in Kelvin (e.g., 1800): '))
    Trange = int(input('Enter the temperature range of interest (e.g., 500 if interested in from 1800 K to 2300 K): '))
    Tinterval = int(input('Enter the interval between temperatures (e.g., 100 if interested in 1800 K, 1900 K, ..., 2300 K): '))

LimitWettingAngle = str(input('Do you want to output only results with the wetting angles in a certain range? (yes or no)'))

if LimitWettingAngle == 'yes':
  LimitType = str(input('Specify the type of limitation (below/above/between): '))
  if LimitType == 'below':
    below = int(input('Enter the maximum wetting angle of interest: '))
  else:
      if LimitType == 'above':
        above = int(input('Enter the minimum wetting angle of interest: '))
      else:
        if LimitType == 'between':
          between1 = int(input('Enter the minimum wetting angle of interest: '))
          between2 = int(input('Enter the maximum wetting angle of interest: '))

outputfilename = str(input('Enter output filename: '))

#================================================================================================
!pip install matminer
!wget http://li.mit.edu/S/SoYeonKim/Upload/WettabilityInputMatrix_Metal-IonocovalentCeramic.csv

#!/usr/bin/env python
import json, sys, os
from urllib.request import urlopen
import pandas as pd
import numpy as np
import matminer
from matminer.utils.conversions import str_to_composition
from matminer.featurizers.composition import ElementProperty
magpie = ElementProperty.from_preset(preset_name="magpie")
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_digits

if option == 2:
  substrate = pd.DataFrame(pd.read_csv(filename)[header].values.tolist())

if option == 3:
  substrate =pd.DataFrame(json.loads(urlopen("http://aflowlib.duke.edu/search/API/?" + MATCHBOOK + ",$paging(0)").read().decode("utf-8")))['compound']

matrix = pd.DataFrame([metal] * len(substrate))

sys_cond_0 = pd.concat([matrix, substrate], axis=1)
sys_cond_0['Temp'] = pd.DataFrame([T0] * len(substrate))
sys_cond_0.columns = ['Metal', 'Substrate', 'Temp']

metal_matminer = pd.DataFrame([metal], columns=['Metal'])
metal_matminer['Me_comp'] = metal_matminer['Metal'].transform(str_to_composition)
data_Me = magpie.featurize_dataframe(metal_matminer, col_id="Me_comp", ignore_errors=True)
metal_features = pd.DataFrame(data_Me.values.tolist()*len(substrate), columns = data_Me.columns)
feature_Me = metal_features.filter(like = 'mean')
feature_Me.columns = ['Me_'+ j for j in feature_Me.columns]

sys_cond_0['Sub_comp'] = sys_cond_0['Substrate'].transform(str_to_composition)
data_Sub = magpie.featurize_dataframe(sys_cond_0, col_id="Sub_comp", ignore_errors=True)
feature_Sub = data_Sub.filter(like = 'mean')
feature_Sub.columns = ['Ce_'+ j for j in feature_Sub.columns]

feature_all = pd.concat([feature_Me, feature_Sub], axis = 1)
sys_feature_0 = pd.concat([sys_cond_0[sys_cond_0.columns[0:3]], feature_all], axis = 1)

sys_feature = sys_feature_0

if Trange != 0:
  for i in range(Trange//Tinterval+1):
    sys_feature_temporary = sys_feature_0 
    T_temporary = pd.DataFrame([T0 + Tinterval * (i)] * len(substrate))
    sys_feature_temporary['Temp'] = T_temporary
    sys_feature = sys_feature.append(sys_feature_temporary)

data = pd.read_csv("WettabilityInputMatrix_Metal-IonocovalentCeramic.csv")
X = data[data.columns[3:]]
y = data['theta']
preds = X.columns[0:]

rf_otm = RandomForestRegressor(n_estimators=400, random_state =51, oob_score = True, max_depth=15, min_samples_split=2)
rf_otm.fit(X[preds], y)

y_sys_pred = rf_otm.predict(sys_feature[preds])
output = sys_feature[sys_feature.columns[0:3]]
output['theta_pred'] = pd.Series(y_sys_pred)

if LimitWettingAngle == 'yes':
  if LimitType == 'below':
    output_lim = output.loc[(output['theta_pred'] < below)]
  else:
      if LimitType == 'above':
        output_lim = output.loc[(output['theta_pred'] > above)]
      else:
        if LimitType == 'between':
          output_lim = output.loc[(output['theta_pred'] > between1) & (output['theta_pred'] < between2)]
        else: print('Error: check if necessary inputs are all entered')
  output_lim.to_csv(outputfilename+'.csv')
else:
  output.to_csv(outputfilename+'.csv')