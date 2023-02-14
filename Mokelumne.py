import pywfm
#import pyhf
import os
import pandas as pd
import numpy as np
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors


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

#let's get nodes
nodes=m.get_node_info()

#These coordinates are in feet, so we need to transform to m to use UTM 10N
nodes['X']=nodes['X']/3.2808
nodes['Y']=nodes['Y']/3.2808

#Let's get stream network
streams=m.get_stream_network()

#stream node ids
strm_node_id=m.get_stream_node_ids()

#mokelumne
mok=streams[streams['ReachName']=='Mokelumne River'].reset_index(drop=True)



#Let's rename to join with node coordinates
mok=mok.rename(columns={"GroundwaterNodes": "NodeID"})


#Let's add coordinates
mok=pd.merge(mok, nodes, how="left", on=["NodeID"])

#let's export to csv
mok.to_csv(os.path.join(shp_out,"Mokelumne.csv"),index=False)

#Let's import nodes within NSJWCD
mok_NSJWCD=pd.read_csv(os.path.join(shp_out,"Mok_NSJWCD.csv")).drop(["index"],axis=1)

#Let's add column for dates
mok_NSJWCD["Date"]=np.nan
#Let's add column for stream gains
mok_NSJWCD['Stream_gain']=np.nan

mok_NSJWCD2=pd.DataFrame(columns=mok_NSJWCD.columns.values)

#Let's loop through timesteps now
while not m.is_end_of_simulation():

    #Let's retrieve the stream-aquifer interaction data
    m.advance_time()
    m.read_timeseries_data()
    m.simulate_for_one_timestep()

    #Let's retrieve stream gain from groundwater
    strm_gain_dum=pd.DataFrame({'StreamNode':strm_node_id,
                                'Stream_gain':m.get_stream_gain_from_groundwater()})
    mok_NSJWCD_dum=mok_NSJWCD.drop(['Stream_gain'],axis=1)
    mok_NSJWCD_dum["Date"]=pd.to_datetime(m.get_current_date_and_time()[0:m.get_current_date_and_time().rfind("_")],format="%m/%d/%Y")
    mok_NSJWCD_dum=pd.merge(mok_NSJWCD_dum, strm_gain_dum, how="left", on=['StreamNode'])
    mok_NSJWCD2=pd.concat([mok_NSJWCD2, mok_NSJWCD_dum], ignore_index=True)
    m.advance_state()

m.kill()

#Let's reshape the dataframe now
mok_NSJWCD2_wide=mok_NSJWCD2.pivot(index='Date',columns='StreamNode',values='Stream_gain')
mok_NSJWCD2_wide.to_csv(os.path.join(csv_out,"Mokelumne_NSJWCD.csv"))

#Let's only select the nodes where the river is gaining
gaining_nodes=np.unique(mok_NSJWCD2.loc[mok_NSJWCD2['Stream_gain']>0,'StreamNode'].values)

mok_gaining=mok_NSJWCD2[mok_NSJWCD2['StreamNode'].isin(gaining_nodes)].reset_index(drop=True)

#Let's convert to AF/month

mok_gaining['Stream_gain']=mok_gaining['Stream_gain']/43560

#Let's convert to wide
mok_gaining_wide=mok_gaining.pivot(index='Date',columns='StreamNode',values='Stream_gain')

mok_gaining_wide.to_csv(os.path.join(csv_out,"Mok_gaining_NSJWCD.csv"))

#Let's filter nodes we are interested in (330 to 370)

nodes_recharge=mok.loc[(mok["StreamNodes"]>=330)&(mok["StreamNodes"]<=370),"StreamNodes"].reset_index(drop=True)

#Dates with gains
dates_with_gains=np.unique(mok_gaining.loc[(mok_gaining['Stream_gain']>0)&(mok_gaining["StreamNode"].isin(nodes_recharge)),"Date"].values)

mok_rech_gain=mok_NSJWCD2[(mok_NSJWCD2["StreamNode"].isin(nodes_recharge))&(mok_NSJWCD2["Date"].isin(dates_with_gains))].reset_index(drop=True)

#Let's convert to AF/month
mok_rech_gain['Stream_gain']=mok_rech_gain['Stream_gain']/43560

for date in dates_with_gains:
    mok_rech_gain[mok_rech_gain["Date"]==date].to_csv(os.path.join(csv_out,"Mok_str_gain"+np.datetime_as_string(date)[0:10]+".csv"))

#Now, let's do it again for Dry Creek

#Dry Creek
stream_name='Dry Creek'
crs='epsg:26910'
bounds=r"P:\Projects\5658_NSJWCD\GIS\Vector\NSJWCD\NSJWCD_26910.shp"
model_version="2_1"

#lines shapefiles for the plots
lines=[["North System",gpd.read_file(r"P:\Projects\5658_NSJWCD\GIS\Vector\NSJWCD\North_System_26910.shp"),"#987db7"]]
polygons=[["Tracy Lake",gpd.read_file(r"P:\Projects\5658_NSJWCD\GIS\Vector\NSJWCD\Tracy_Lake_26910.shp"),"#1f78b4"]]

stream=streams[streams['ReachName']=='Dry Creek'].reset_index(drop=True)
stream=stream.rename(columns={"GroundwaterNodes": "NodeID"})
#Let's add coordinates
stream=pd.merge(stream, nodes, how="left", on=["NodeID"])
#let's export to csv
stream.to_csv(os.path.join(shp_out,stream_name+".csv"),index=False)
geometry = [Point(xy) for xy in zip(stream.X, stream.Y)]
geo_df = gpd.GeoDataFrame(stream, crs=crs, geometry=geometry)
#Let's export to shapefile
geo_df.to_file(os.path.join(shp_out,"nodes.shp"))

#Let's import shapefile with boundaries
bounds_gdf=gpd.read_file(bounds)

#Let's only select nodes within the NSJWCD
geo_df=geo_df[geo_df.geometry.within(bounds_gdf.geometry[0])]

#Let's add column for dates
geo_df["Date"]=np.nan
#Let's add column for stream gains
geo_df['Stream_gain']=np.nan

#Let's create empty geodataframe now
geo_df2=gpd.GeoDataFrame(columns=geo_df.columns)

#Let's loop through timesteps now
while not m.is_end_of_simulation():

    #Let's retrieve the stream-aquifer interaction data
    m.advance_time()
    m.read_timeseries_data()
    m.simulate_for_one_timestep()

    #Let's retrieve stream gain from groundwater
    strm_gain_dum=pd.DataFrame({'StreamNodes':strm_node_id,
                                'Stream_gain':m.get_stream_gain_from_groundwater()})
    geo_df_dum=geo_df.drop(['Stream_gain'],axis=1)
    geo_df_dum["Date"]=pd.to_datetime(m.get_current_date_and_time()[0:m.get_current_date_and_time().rfind("_")],format="%m/%d/%Y")
    geo_df_dum=pd.merge(geo_df_dum, strm_gain_dum, how="left", on=['StreamNodes'])
    geo_df2=pd.concat([geo_df2, geo_df_dum], ignore_index=True)
    m.advance_state()

m.kill()

#Let's convert to AF/month
geo_df2['Stream_gain']=geo_df2['Stream_gain']/43560

#Maximum gain
max_dum = np.max(np.abs(geo_df2.Stream_gain))

dates=np.unique(geo_df2.Date)

ts=dates[0]

for j in range(len(dates)):
    #Geodataframe for that time step
    geo_df_ts=geo_df2[geo_df2.Date==dates[j]].copy()

    #Let's add size
    geo_df_ts["size"]=np.abs(10*geo_df_ts.Stream_gain.values/max_dum)


    #Let's start plot
    fig, ax = plt.subplots(figsize=(16, 9))

    for i in range(len(lines)):
        lines[i][1].plot(ax=ax,color=lines[i][2],linewidth=0.5,label=lines[i][0], lw=2)

    for i in range(len(polygons)):
        polygons[i][1].plot(ax=ax,facecolor=polygons[i][2],label=polygons[i][0])

    plt.scatter(geo_df_ts.X,geo_df_ts.Y,s=geo_df_ts["size"],marker='o',norm=colors.Normalize(vmin=-max_dum, vmax=max_dum),cmap='coolwarm',c=geo_df_ts.Stream_gain)


    plt.savefig(os.path.join(dir_out, "Gain_from_GW_"+model_version+"_"+np.datetime_as_string(ts)[:10].replace("-","_")+".png"))
    plt.close()