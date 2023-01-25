import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyhf
import pywfm
import geopandas as gpd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

#Path to ESJWRM 2.2
model_path=r"C:\Projects\5658\ESJWRM Version 2.2 modified"
#preprocessor file
preprocessor_in_file=os.path.join(model_path,r"Preprocessor\PreProcessor_MAIN.IN")

#simulation file
simulation_in_file = os.path.join(model_path,r"Simulation\Simulation_MAIN.IN")

#Velocities file
velocities_path=r"C:\Projects\5658\ESJWRM Version 2.2 modified\Results\Velocities - Copy.out"
Centroids_Flag="*  ELEMENT                 X                 Y"
velocities_flag="*                              *          VELOCITIES AT CELL CENTROIDS          *"
dir_out=r'P:\Projects\5658_NSJWCD\ESJWRM_v2_2\Velocities'


m = pywfm.IWFMModel(preprocessor_in_file, simulation_in_file)

time_steps=m.get_time_specs()
nnodes=m.get_n_nodes()

m.kill()

#First, let's do version 2.1
model_version="2_1"
velocities_path=r"P:\Projects\5658_NSJWCD\IWRFM\ESJWRM Version 2.1\Results\Velocities - Copy.out"
#Mokelumne
mok=gpd.read_file(r"P:\Projects\5658_NSJWCD\GIS\Vector\Mok.shp")
North_system=gpd.read_file(r"P:\Projects\5658_NSJWCD\GIS\Vector\North_System_UTM10N.shp")
South_System=gpd.read_file(r"P:\Projects\5658_NSJWCD\GIS\Vector\SouthSystem_UTM10N.shp")
Tracy_Lake=gpd.read_file(r"P:\Projects\5658_NSJWCD\GIS\Vector\TracyLake_UTM10N.shp")
Costa=gpd.read_file(r"P:\Projects\5658_NSJWCD\GIS\Vector\Costa_Vineyard_UTM_10N.shp")
Tecklenburg=gpd.read_file(r"P:\Projects\5658_NSJWCD\GIS\Vector\Tecklenburg_UTM10N.shp")

model_version="2_1"
ts=time_steps[0][-1]
for ts in time_steps[0]:
    pyhf.utils.iwfm_velocities(velocities_path,
                               time_flag=ts,
                               dir_out=dir_out,
                               n_elements=nnodes,
                               model_version="2_1")

    velocities = pd.read_csv(os.path.join(r"P:\Projects\5658_NSJWCD\ESJWRM_v2_2\Velocities","Velocities_"+model_version+"_"+ts.replace("/","_").replace(":","_")+".csv"))
    fig, ax = plt.subplots(figsize=(16, 9))

    mok.plot(ax=ax, color="#1f78b4", linewidth=0.5, lw=2)
    North_system.plot(ax=ax, color="#987db7", linewidth=0.5, label='North System', lw=2)
    South_System.plot(ax=ax, facecolor="none", edgecolor="#ff7f00", label='South System')
    Tracy_Lake.plot(ax=ax, facecolor="#1f78b4", label='Tracy Lake')
    Costa.plot(ax=ax, facecolor="#6a3d9a", label='Costa Vineyard')
    Tecklenburg.plot(ax=ax, facecolor="#a6cee3", label='Tecklenburg')
    ax.quiver(velocities["X"], velocities["Y"], velocities['Lay1_VX'], velocities['Lay1_VY'], color='r',
              scale=0.01)
    legend_elements = [Line2D([0], [0], color="#1f78b4", lw=4, label='Mokelumne River'),
                       Line2D([0], [0], color="#987db7", lw=4, label='North System'),
                       Patch(facecolor='none', edgecolor="#ff7f00",
                             label='South System'),
                       Patch(facecolor='#1f78b4',
                             label='Tracy Lake'),
                       Patch(facecolor='#6a3d9a',
                             label='Costa Vineyard'),
                       Line2D([0], [0], marker='o', color='#a6cee3', label='Tecklenburg',
                              markersize=15)]

    ax.legend(handles=legend_elements)

    plt.xlim(643190, 664183)
    plt.ylim(4212700, 4232350)
    plt.axis('off')

    plt.savefig(os.path.join(dir_out, "Velocities_"+model_version+"_"+ts.replace("/","_").replace(":","_")+".png"))
    plt.close()

#Now, version 2.2
model_version="2_2"
velocities_path=r"C:\Projects\5658\ESJWRM Version 2.2 modified\Results\Velocities - Copy.out"

ts=time_steps[0][-1]
for ts in time_steps[0]:
    pyhf.utils.iwfm_velocities(velocities_path,
                               time_flag=ts,
                               dir_out=dir_out,
                               n_elements=nnodes,
                               model_version="2_2")

    velocities = pd.read_csv(os.path.join(r"P:\Projects\5658_NSJWCD\ESJWRM_v2_2\Velocities","Velocities_"+model_version+"_"+ts.replace("/","_").replace(":","_")+".csv"))
    fig, ax = plt.subplots(figsize=(16, 9))

    mok.plot(ax=ax, color="#1f78b4", linewidth=0.5, lw=2)
    North_system.plot(ax=ax, color="#987db7", linewidth=0.5, label='North System', lw=2)
    South_System.plot(ax=ax, facecolor="none", edgecolor="#ff7f00", label='South System')
    Tracy_Lake.plot(ax=ax, facecolor="#1f78b4", label='Tracy Lake')
    Costa.plot(ax=ax, facecolor="#6a3d9a", label='Costa Vineyard')
    Tecklenburg.plot(ax=ax, facecolor="#a6cee3", label='Tecklenburg')
    ax.quiver(velocities["X"], velocities["Y"], velocities['Lay1_VX'], velocities['Lay1_VY'], color='r',
              scale=0.01)
    legend_elements = [Line2D([0], [0], color="#1f78b4", lw=4, label='Mokelumne River'),
                       Line2D([0], [0], color="#987db7", lw=4, label='North System'),
                       Patch(facecolor='none', edgecolor="#ff7f00",
                             label='South System'),
                       Patch(facecolor='#1f78b4',
                             label='Tracy Lake'),
                       Patch(facecolor='#6a3d9a',
                             label='Costa Vineyard'),
                       Line2D([0], [0], marker='o', color='#a6cee3', label='Tecklenburg',
                              markersize=15)]

    ax.legend(handles=legend_elements)

    plt.xlim(643190, 664183)
    plt.ylim(4212700, 4232350)
    plt.axis('off')

    plt.savefig(os.path.join(dir_out, "Velocities_"+model_version+"_"+ts.replace("/","_").replace(":","_")+".png"))
    plt.close()



#Let's import nodes coordinates
nodes=pd.read_csv(os.path.join(dir_out,'Nodes_Coordinates.csv'))



date="09_30_2020_24_00"
velocities=pd.read_csv(r"P:\Projects\5658_NSJWCD\ESJWRM_v2_2\Velocities\09_30_2020_24_00.csv")

fig, ax = plt.subplots(figsize=(16, 9))





mok.plot(ax=ax,color="#1f78b4",linewidth=0.5, lw=2)
North_system.plot(ax=ax,color="#987db7",linewidth=0.5,label='North System', lw=2)
South_System.plot(ax=ax,facecolor="none",edgecolor="#ff7f00",label='South System')
Tracy_Lake.plot(ax=ax,facecolor="#1f78b4",label='Tracy Lake')
Costa.plot(ax=ax,facecolor="#6a3d9a",label='Costa Vineyard')
Tecklenburg.plot(ax=ax,facecolor="#a6cee3",label='Tecklenburg')
ax.quiver(velocities["X_UTM10N"], velocities["Y_UTM10N"], velocities['Vx_1'], velocities['Vy_1'], color='r',scale=0.01)
legend_elements = [Line2D([0], [0], color="#1f78b4", lw=4, label='Mokelumne River'),
                   Line2D([0], [0], color="#987db7", lw=4, label='North System'),
                   Patch(facecolor='none',edgecolor="#ff7f00",
                         label='South System'),
                   Patch(facecolor='#1f78b4',
                         label='Tracy Lake'),
                   Patch(facecolor='#6a3d9a',
                         label='Costa Vineyard'),
                   Line2D([0], [0], marker='o', color='#a6cee3', label='Tecklenburg',
                          markersize=15)]

ax.legend(handles=legend_elements)

plt.xlim(643190,664183)
plt.ylim(4212700,4232350)
plt.axis('off')



plt.savefig(os.path.join(dir_out,"velocities_"+".png"))
plt.close()




velocities.to_csv(os.path.join(dir_out,date.replace("/","_").replace(":","_")+".csv"))



with open(velocities_path) as f:
    lines = f.readlines()

#dates

dates=["09/30/2020_24:00"]

#Let's find the first time step
i=0
date=dates[0]
while lines[i].find(date):
    i+=1


line=lines[i]
#Let's remove \n
line=line[:-1]

#Let's split
line=line.split(" ")

#Let's remove empty values
line=[item for item in line if item != ""]

#Let's remove date
line=line[1:]

#Let's start dataframe
velocities=pd.DataFrame({"NodeID":[line[0]],
                         "Vx_1":[line[1]],
                         "Vy_1":[line[2]],
                         "Vz_1":[line[3]],
                         "Vx_2": [line[4]],
                         "Vy_2": [line[5]],
                         "Vz_2": [line[6]],
                         "Vx_3": [line[7]],
                         "Vy_3": [line[8]],
                         "Vz_3": [line[9]],
                         "Vx_4": [line[10]],
                         "Vy_4": [line[11]],
                         "Vz_4": [line[12]],
                         })

#Number of nodes
nnodes=  16054
i+=1
for j in range(nnodes-1):
    line = lines[i]
    # Let's remove \n
    line = line[:-1]

    # Let's split
    line = line.split(" ")

    # Let's remove empty values
    line = [item for item in line if item != ""]

    # Let's start dataframe
    velocities_dum = pd.DataFrame({"NodeID": [line[0]],
                               "Vx_1": [line[1]],
                               "Vy_1": [line[2]],
                               "Vz_1": [line[3]],
                               "Vx_2": [line[4]],
                               "Vy_2": [line[5]],
                               "Vz_2": [line[6]],
                               "Vx_3": [line[7]],
                               "Vy_3": [line[8]],
                               "Vz_3": [line[9]],
                               "Vx_4": [line[10]],
                               "Vy_4": [line[11]],
                               "Vz_4": [line[12]],
                               })
    velocities=pd.concat([velocities, velocities_dum], ignore_index=True)

    i += 1

#Let's join coordinates
velocities["NodeID"]=velocities["NodeID"].astype(int)
velocities.loc[:,velocities.columns!="NodeID"]=velocities.loc[:,velocities.columns!="NodeID"].astype(float)
velocities=pd.merge(nodes, velocities, how="left", on=['NodeID'])

plt.quiver(velocities["X_UTM10N"], velocities["Y_UTM10N"], velocities['Vx_1'], velocities['Vy_1'], color='g',scale=0.05)

plt.xlim(637507,682783)
plt.ylim(4209224,4244046)

plt.close()

velocities.to_csv(os.path.join(dir_out,date.replace("/","_").replace(":","_")+".csv"))

