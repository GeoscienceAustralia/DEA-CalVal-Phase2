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

    if isinstance(in_df.Line, int):
        looper = [in_df.Line]
    else:
        looper = in_df.Line.unique()

    for i in looper:
        temp_loop = in_df[(in_df['Wavelength']==350) & (in_df['Line']==i)]
        for j in temp_loop.Spec_number.unique():
            temp2 = in_df[(in_df['Spec_number']==j) & (in_df['Line']==i)]
            
            try:
                out_df['radiance'+str(i)+"-"+str(j)] = temp2['radiance']
            except UnboundLocalError:
                out_df = temp2[['Wavelength', 'radiance']].copy()

    out_df.set_index("Wavelength", inplace=True)

    return out_df

