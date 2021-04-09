import json, sys, os
from urllib.request import urlopen
import pandas as pd
import numpy as np
import matminer
from matminer.featurizers.conversions import StrToComposition
from matminer.featurizers.composition import ElementProperty
magpie = ElementProperty.from_preset(preset_name="magpie")
import sklearn
from sklearn.ensemble import RandomForestRegressor

# The first step is to specify the type of estimation you would like to perform. Please choose one of the options.
option = 1 # 1: one metal-ceramic pair; 2: metal-list of ceramics; or 3: ICSD screening

#===================================================================================
# The second step is to specify the systems of interest.
# Note that this code is case sensitive. You need to enter "Fe" for iron; "fe" does not work.
# Also, you need to enter "Si1O2" for silicon dioxide; "SiO2" does not work.
# Enter the metal of interest (e.g., "Fe"): 
metal = "Fe"

if option == 1: # If you chose "1" for the option above, enter the ceramic of interest below (e.g., "Si1O2").
  substrate = pd.DataFrame(["Si1O2"])
else:
    if option == 2: # If you chose "2" for the option above, upload the csv file with the list of ceramics to the session storage and enter the filename and the header.
      substrate = pd.DataFrame(pd.read_csv("filename.csv")["header for the ceramic list"].values.tolist())
    else: 
        if option == 3: # If you chose "3" for the option above, you need to enter material keywords and arguments to retrieve ceramics that satisfy certain criteria. 
                        # Please refer to the Figure 1 and the Appendix C of the following article: https://doi.org/10.1016/j.commatsci.2017.04.036.
                        # For example, to retrieve compounds with O or F but no S of which the number of species is between 2 and 8, "species((O:F),!S),nspecies(2*,*8),catalog(icsd)" should be used.
          MATCHBOOK="species((O:F),!S),nspecies(2*,*8),catalog(icsd)"
        else: print('Error: check if necessary inputs are all entered.')

#===================================================================================
# The third step is to specify the temperature range of interest.
# For example, if you are interested in wetting angles at 1800 K, 1900 K, 2000 K, 2100 K, and 2200 K, enter 1800 for T0, 500 for Trange, and 100 for Tinterval.
T0 = 1800 # in Kelvin
Trange = 500 # Enter 0 if only the wetting angles at T0 is of interest.
Tinterval = 100

#===================================================================================
# Next step is to specify the wetting angle range of interest.
# For example, if you would like to see only the results for the pairs of which wetting angles are between 50 degree and 100 degree, 
# enter "yes" for LimitWettingAngle and "50-100" for WettingAngle Range.
LimitWettingAngle = "yes" # "yes" or "no"
WettingAngleRange = "0-180" # e.g., "50-"", "-100", or "50-100"

#===================================================================================
# Finally, enter the desired output filename (e.g., "result")
outputfilename = "result"

#===================================================================================
data = pd.read_csv("input-matrix.csv")
X = data[data.columns[3:]]
y = data['theta']
preds = X.columns[0:]

rf_otm = RandomForestRegressor(n_estimators=400, random_state =51, oob_score = True, max_depth=15, min_samples_split=2)
rf_otm.fit(X[preds], y)

if option == 3:
  substrate =pd.DataFrame(json.loads(urlopen("http://aflowlib.duke.edu/search/API/?" + MATCHBOOK + ",$paging(0)").read().decode("utf-8")))['compound']

matrix = pd.DataFrame([metal] * len(substrate))

sys_cond_0 = pd.concat([matrix, substrate], axis=1)
sys_cond_0['Temp'] = pd.DataFrame([T0] * len(substrate))
sys_cond_0.columns = ['Metal', 'Substrate', 'Temp']

metal_matminer = pd.DataFrame([metal], columns=['Metal'])
metal_matminer = StrToComposition(target_col_id='Me_comp').featurize_dataframe(metal_matminer, 'Metal')
data_Me = magpie.featurize_dataframe(metal_matminer, col_id="Me_comp", ignore_errors=True)
metal_features = pd.DataFrame(data_Me.values.tolist()*len(substrate), columns = data_Me.columns)
feature_Me = metal_features.filter(like = 'mean')
feature_Me.columns = ['Me_'+ j for j in feature_Me.columns]

sys_cond_0 = StrToComposition(target_col_id='Sub_comp').featurize_dataframe(sys_cond_0, 'Substrate')
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

y_sys_pred = rf_otm.predict(sys_feature[preds])
output = sys_feature[sys_feature.columns[0:3]]
output['theta_pred'] = pd.Series(y_sys_pred)

if LimitWettingAngle == 'yes':
  WAsplit = WettingAngleRange.split('-')
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