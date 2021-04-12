import pandas as pd
import numpy as np
import joblib
import json, sys, os
from urllib.request import urlopen
import matminer
from matminer.featurizers.conversions import StrToComposition
from matminer.featurizers.composition import ElementProperty
magpie = ElementProperty.from_preset(preset_name="magpie")

print('The first step is to specify the type of estimation and machine learning model you would like to use.')
option = int(input('Enter type (1: one metal-one ceramic pair; 2: one metal-list of ceramics; 3: ICSD screening): '))
model = str(input('Enter model (all: model trained using all features; reduced: model trained using a reduced number of features): '))

print('=====================================================================')
print('The second step is to specify the systems of interest.')
print('Note that this code is case sensitive. You need to enter "Fe" for iron; "fe" does not work.') 
print('Also, you need to enter "Si1O2" for silicon dioxide; "SiO2" does not work.')
metal = str(input('Enter the metal of interest (e.g., Fe): '))

if option == 1:
  ceramic = str(input('Enter the ceramic of interest (e.g., Si1O2): '))
  substrate = pd.DataFrame([ceramic])
else:
    if option == 2:
      filename = str(input('Upload the csv file with the list of ceramics to the session storage and enter the filename (e.g., filename.csv): '))
      header = str(input('Enter the header of the list of ceramics (e.g., ceramic): '))
    else: 
        if option == 3:
          MATCHBOOK = str(input('Enter the MATCHBOOK referring to https://doi.org/10.1016/j.commatsci.2017.04.036 (e.g.,species((O:F),!S),nspecies(2*,*8),catalog(icsd))'))
        else: print('Error: check if necessary inputs are all entered.')

print('=====================================================================')
print('The third step is to specify the temperature range of interest.')
Trange = str(input('Enter the temperature of interest in Kelvin in the format, "min-max-interval (e.g., 1800-1800-0 or 1800-2300-100)": '))

print('=====================================================================')
print('The final step is to specify the wetting angle range of interest.')
WArange = str(input('Specify the wetting angle range of interest (e.g., all, 50-, -100, or 50-100): '))

outputfilename = str(input('Enter output filename (e.g., result): '))

#================================================================================================
if option == 2:
  substrate = pd.DataFrame(pd.read_csv(filename)[header].values.tolist())

if option == 3:
  substrate = pd.DataFrame(json.loads(urlopen("http://aflowlib.duke.edu/search/API/?" + MATCHBOOK + ",$paging(0)").read().decode("utf-8")))['compound']

matrix = pd.DataFrame([metal] * len(substrate))

Tsplit = [float(i) for i in Trange.split('-')]
if Tsplit[2] != 0:
  Tlist = np.arange(Tsplit[0], Tsplit[1], Tsplit[2]).tolist()

sys_cond_0 = pd.concat([matrix, substrate], axis=1)
sys_cond_0['Temp'] = pd.DataFrame([Tsplit[0]] * len(substrate))
sys_cond_0.columns = ['Metal', 'Substrate', 'Temp']

metal_matminer = pd.DataFrame([metal], columns=['Metal'])
metal_matminer = StrToComposition(target_col_id='Me_comp').featurize_dataframe(metal_matminer, 'Metal')
data_Me = magpie.featurize_dataframe(metal_matminer, col_id="Me_comp", ignore_errors=True)
metal_features = pd.DataFrame(data_Me.values.tolist()*len(substrate), columns = data_Me.columns)
feature_Me = metal_features.filter(like = 'mean')
feature_Me = feature_Me.drop(columns=['MagpieData mean NfUnfilled'])
feature_Me.columns = ['Me_'+ j for j in feature_Me.columns]

sys_cond_0 = StrToComposition(target_col_id='Sub_comp').featurize_dataframe(sys_cond_0, 'Substrate')
data_Sub = magpie.featurize_dataframe(sys_cond_0, col_id="Sub_comp", ignore_errors=True)
feature_Sub = data_Sub.filter(like = 'mean')
feature_Sub.columns = ['Ce_'+ j for j in feature_Sub.columns]

feature_all = pd.concat([feature_Me, feature_Sub], axis = 1)
sys_feature_0 = pd.concat([sys_cond_0[sys_cond_0.columns[0:3]], feature_all], axis = 1)

sys_feature = sys_feature_0

if Tsplit[2] != 0:
  for i in Tlist:
    sys_feature_temporary = sys_feature_0 
    T_temporary = pd.DataFrame([i] * len(substrate))
    sys_feature_temporary['Temp'] = T_temporary
    sys_feature = sys_feature.append(sys_feature_temporary) 

preds = sys_feature.columns[2:]

rf_otm = joblib.load('https://github.com/sokim1/Wettability_Metal-IonocovalentCeramic/blob/a3042245e15c6b308ff4e72024d6b5addff2dcf3/prediction/wap_'+ model + '.sav')
if model == 'reduced':
  preds = ['Temp', 'Me_MagpieData mean CovalentRadius',
       'Me_MagpieData mean Electronegativity', 'Me_MagpieData mean NdValence',
       'Me_MagpieData mean GSmagmom', 'Me_MagpieData mean SpaceGroupNumber',
       'Ce_MagpieData mean MeltingT', 'Ce_MagpieData mean NpUnfilled']

y_sys_pred = rf_otm.predict(sys_feature[preds])
y_sys_pred = [round(i, 1) for i in y_sys_pred]
output = sys_feature[sys_feature.columns[0:3]]
output['theta_pred'] = pd.Series(y_sys_pred)

output = output.drop_duplicates()

if not WArange == 'all':
  WAsplit = WArange.split('-')
  if WAsplit[0].isnumeric():
    if WAsplit[1].isnumeric():
      output_lim = output.loc[(output['theta_pred'] > float(WAsplit[0])) & (output['theta_pred'] < float(WAsplit[1]))]
    else: 
      output_lim = output.loc[(output['theta_pred'] > float(WAsplit[0]))]
  else:
    output_lim = output.loc[(output['theta_pred'] < float(WAsplit[1]))]
  output_lim.to_csv(outputfilename+'.csv')
else:
  output.to_csv(outputfilename+'.csv')

print('=====================================================================')
print('Prediction complete!')
print('The CSV file with the results is stored in the session storage.')