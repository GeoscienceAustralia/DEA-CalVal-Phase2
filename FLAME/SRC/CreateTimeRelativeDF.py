import numpy as np
from datetime import timedelta


#
### Create dataframe with relative time stamps
#
# Make a new dataframe with time since the first good panel reading
# along the x-axis and "1" for the y-axis. This allows a plot of the
# data timeline to be made.
#
def make_timeline(in_df, all_panels):
    
    temp_df = in_df[['filename', 'Line', 'date_saved']].loc[in_df['Wavelength']==450]
    gpt = all_panels[['date_saved', 'Line']].loc[all_panels['Wavelength']==450]
    
    out_df = temp_df.copy()

    for i in range(len(out_df)):
        out_df.iloc[[i], [0]]=int((temp_df.iloc[i][2]-gpt.iloc[0][0]).total_seconds())

    out_df.rename({'filename': 'Time'}, axis=1, inplace=True)
    out_df['ones'] = np.ones(len(out_df))
    return out_df

#
### Create time-relative dataframes
#
#   gpt = good panels
#   gpta = all panels
#   adt = good grounds
#   adta = all grounds
#
def create_time_relative_dfs(all_panels, all_grounds):
    
    gpta = make_timeline(all_panels, all_panels)
    adta = make_timeline(all_grounds, all_panels)
    
    return gpta, adta
