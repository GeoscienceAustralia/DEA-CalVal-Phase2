import pandas as pd
import numpy as np


#
# Bin spectra into integer wavelength bins, assuming that the input data
# has 0.3nm channels.
#
def wavelength_bin(alldata):
    # Create avgdata DataFrame, based on alldata input DataFrame
    # Reset index so that Wavelength is not the index.
    avgdata = alldata.copy()
    avgdata.reset_index(inplace=True)
    
    ### Make a mean of three rows for each of DN, Calibration, Radiance
    ###avgdata['DNmean'] = avgdata.DN.rolling(3, center=True).mean()
    ###avgdata['Calmean'] = avgdata.CalData.rolling(3, center=True).mean()
    ###avgdata['Radmean'] = avgdata.radiance.rolling(3, center=True).mean()
    
    # Remove first and last wavelengths which have NaNs in them.
    avgdata = avgdata[avgdata.Wavelength != 349.176]
    avgdata = avgdata[avgdata.Wavelength != 910.925]
    
    # Create empty output DataFrame
    outputDF = pd.DataFrame()
    ttmm = pd.DataFrame()
    
    # Loop through each spectrum in the dataframe
    for j in avgdata.SpecNum.unique():
        tempdata = avgdata[avgdata.SpecNum==j].groupby(pd.cut(avgdata[avgdata.SpecNum==j]['Wavelength'], np.arange(349.5,910.5,1.0))).mean()
        tempdata['date_saved'] = avgdata[avgdata.SpecNum==j].date_saved.values[0]
        tempdata['filename'] = avgdata[avgdata.SpecNum==j].filename.values[0]
        
        tempdata.index.rename('plop', inplace=True)
        tempdata.reset_index(inplace=True)
        tempdata.drop(columns='plop', inplace=True)
        tempdata.Wavelength = tempdata.Wavelength.round(0).astype(int)        
        
        # When finished making an entire spectrum, add it to the output DataFrame
        # and print how many have been done.
        if outputDF.empty:
            outputDF = tempdata.copy()
        
        else:
            if j % 100 == 0:
                ttmm = pd.concat([ttmm, tempdata])
                outputDF = pd.concat([outputDF, ttmm])
                ttmm = pd.DataFrame()
            
            elif j == len(avgdata.SpecNum.unique())-1:
                ttmm = pd.concat([ttmm, tempdata])
                outputDF = pd.concat([outputDF, ttmm])
            
            elif ttmm.empty:
                ttmm = tempdata.copy()
            
            else:
                ttmm = pd.concat([ttmm, tempdata])
                
            
        print('Completed ', j+1, '/', len(avgdata.SpecNum.unique()), ' spectra', end='\r', flush=True)

    # output final DataFrame
    return outputDF
