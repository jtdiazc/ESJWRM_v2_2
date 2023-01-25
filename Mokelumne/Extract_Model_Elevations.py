import pywfm
#import pyhf
import os
import pandas as pd
import numpy as np


#Path to ESJWRM 2.2
model_path=r"C:\Projects\5658\ESJWRM Version 2.2 modified"

#preprocessor file
preprocessor_in_file=os.path.join(model_path,r"Preprocessor\PreProcessor_MAIN.IN")

#simulation file
simulation_in_file = os.path.join(model_path,r"Simulation\Simulation_MAIN.IN")

#Path to csv folder
csv_path=r"P:\Projects\5658_NSJWCD\ESJWRM_v2_2"


# create instance of the IWFMModel class
m = pywfm.IWFMModel(preprocessor_in_file, simulation_in_file)

#Let's import new wells
new_wells=pd.read_csv(os.path.join(csv_path,"New_Wells.csv"))

new_wells_names=new_wells['Name']

new_wells_layers=pd.DataFrame(columns=['Name','HYDROGRAPH ID','Top','L1_bot','L2_bot','L3_bot','L4_bot'])

for well in new_wells_names:
    x_dum=new_wells.loc[new_wells['Name']==well,'X'].values[0]
    y_dum=new_wells.loc[new_wells['Name']==well,'Y'].values[0]
    stat_dum=m.get_stratigraphy_atXYcoordinate(x_dum,y_dum,fact=3.2808)
    new_wells_layers_dum=pd.DataFrame({'Name':[well],
                                       'HYDROGRAPH ID':[new_wells.loc[new_wells['Name']==well,'ID'].values[0]],
                                       'Top':[stat_dum[0]],
                                       'L1_bot':[stat_dum[1]],
                                       'L2_bot':[stat_dum[2]],
                                       'L3_bot':[stat_dum[3]],
                                       'L4_bot':[stat_dum[4]]})
    new_wells_layers=pd.concat([new_wells_layers, new_wells_layers_dum], ignore_index=True)

new_wells_layers.to_csv(os.path.join(csv_path,"New_Wells_Layers.csv"))