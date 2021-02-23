import pandas as pd
#
### Make a dataframe that contains just the spectra, with one spectrum per column
#
# Loop over each line 'i' and then over each spectrum 'j' within line 'i'.
# 
# For the first spectrum, copy both the
# Wavelength (for the index) and radiance to a new dataframe (temp2).
# For all subsequent spectra, append the new dataframe with a radiance
# column. The results in a new dataframe 'outpanel' that has a wavelength
# column (also set as the index), plus all the radiances in subsequent
# columns.
#
def make_spec_df(in_df):

    out_df = pd.DataFrame()
    for j in in_df['SpecNum'].unique():
        temp2 = in_df[in_df['SpecNum']==j]
         
        if not out_df.empty:
            temp2.set_index('Wavelength', inplace=True)
            out_df['radiance'+"-"+str(j)] = temp2['radiance']
        else:
            out_df = temp2[['Wavelength', 'radiance']].copy()
            out_df.set_index("Wavelength", inplace=True)

    return out_df

