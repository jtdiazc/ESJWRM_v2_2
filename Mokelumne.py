import pywfm
#import pyhf
import os
import pandas as pd
import numpy as np


#Path to ESJWRM 2.2
model_path=r"C:\Projects\5658\ESJWRM Version 2.2 modified"

#Shapefiles output path
shp_out=r"P:\Projects\5658_NSJWCD\GIS\Vector\Model Shapefiles\Streams"

#Output path for csvs
csv_out=r"P:\Projects\5658_NSJWCD\ESJWRM_v2_2\Mokelumne"


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

