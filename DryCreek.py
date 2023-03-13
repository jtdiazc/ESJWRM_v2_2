import pywfm
import pyhf
import os
import pandas as pd
import numpy as np
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage


#Path to ESJWRM 2.2
model_path=r"C:\Users\jdiaz\OneDrive - HydroFocus\5658_old\ESJWRM Version 2.2 modified"

#Shapefiles output path
shp_out=r"C:\Users\jdiaz\OneDrive - HydroFocus\5658\ESJWRM_v2_2\Gain_from_GW\Vector"

#Output path for csvs
csv_out=r"C:\Users\jdiaz\OneDrive - HydroFocus\5658\ESJWRM_v2_2\Gain_from_GW\CSV"

dir_out=r"C:\Users\jdiaz\OneDrive - HydroFocus\5658\ESJWRM_v2_2\Gain_from_GW"


#preprocessor file
preprocessor_in_file=os.path.join(model_path,r"Preprocessor\PreProcessor_MAIN.IN")

#simulation file
simulation_in_file = os.path.join(model_path,r"Simulation\Simulation_MAIN.IN")




for stream_name in ['Mokelumne River','Dry Creek']:
    # create instance of the IWFMModel class
    m = pywfm.IWFMModel(preprocessor_in_file, simulation_in_file)
    pyhf.utils.iwfm_gaining(m,stream_name,
                            shp_out=shp_out,
                            bounds=os.path.join(shp_out,"NSJWCD_26910.shp"),
                            im_path=os.path.join(dir_out,"Background.png"),
                            dir_out=dir_out)

