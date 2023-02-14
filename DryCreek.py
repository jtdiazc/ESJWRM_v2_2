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
model_path=r"C:\Projects\5658\ESJWRM Version 2.2 modified"

#Shapefiles output path
shp_out=r"P:\Projects\5658_NSJWCD\GIS\Vector\Model Shapefiles\Streams"

#Output path for csvs
csv_out=r"P:\Projects\5658_NSJWCD\ESJWRM_v2_2\Mokelumne"

dir_out=r"P:\Projects\5658_NSJWCD\ESJWRM_v2_2\Dry_Creek"


#preprocessor file
preprocessor_in_file=os.path.join(model_path,r"Preprocessor\PreProcessor_MAIN.IN")

#simulation file
simulation_in_file = os.path.join(model_path,r"Simulation\Simulation_MAIN.IN")

# create instance of the IWFMModel class
m = pywfm.IWFMModel(preprocessor_in_file, simulation_in_file)

stream_name='Dry Creek'
pyhf.utils.iwfm_gaining(m,stream_name)

