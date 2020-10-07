import matplotlib.pyplot as plt
import pandas as pd


#
## Figure 
#
### Plot ground spectra (all and good), normalised to the median good spectrum
#
# These plots are used to identify any ground spectra that are bogus.
#
def FIG_ground_spectra(all_grounds_spec, output, field_data, fignum):

    if isinstance(all_grounds_spec, pd.DataFrame):
        all_median = all_grounds_spec.median(axis=1)
        all_norm = all_grounds_spec.div(all_median, axis=0)

        fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5.5, 5.5))
        plt.tight_layout(pad=5.5, w_pad=1.0, h_pad=1.0)

        all_grounds_spec.plot(title="All ground radiances", legend=False, ax=axes)
        axes.set_xlabel('Wavelength (nm)')
        axes.set_ylabel('Radiance (W m$^{-2}$ nm$^{-1}$ sr$^{-1}$)')

        plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_GroundRadiances.png')
