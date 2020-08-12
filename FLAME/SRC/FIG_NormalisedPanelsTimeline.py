import numpy as np
import matplotlib.pyplot as plt


#
## Figure 
#
### Create timeline plot of averaged, normalised all/good panels
#
#    These plots are used to identify any panels that show unusually bright or
#    dark readings, which can be weeded out as bad panels.
#    
# The general shape of the curve should follow "insolation" - the changing of
# incident light due to the Sun rising/falling in the sky.
#
# The method to create the normalised mean panels is as follows:
#
#    1. A mask of the mean good panels is created that removes the wavelengths
#       that are most affected by low atmospheric transmission.
#    2. ALL/GOOD spectra are divided by the masked mean good panel spectrum to
#       make normalised spectra. CURRENTLY NO NORMALISATION IS APPLIED
#    3. The mean values for both ALL and GOOD normalised spectra are created.
#    4. The mean values for spectra are appended to the gpt and gpta dataframes.
#    5. The mean values are plotted, as a function of time, relative to the
#       first panel time stamp.
#
def normalise_spectra(all_panel_mean, all_panel_spec, gpta, field_data):


    # 1.
    mean_panel_masked = all_panel_mean.where(np.logical_and(all_panel_mean.index>450, all_panel_mean.index<550))
    #mean_panel_masked = all_panel_mean.copy()

    # 2. (NO NORMALISATION)
    all_norm_panels_masked = all_panel_spec.div(mean_panel_masked, axis=0)
    all_panels_masked = all_norm_panels_masked.multiply(mean_panel_masked, axis=0)

    # 3.
    all_averages_masked = all_panels_masked.mean(axis=0)

    # 4.
    gpta['Averaged_Panels']=all_averages_masked.values
    
    return gpta

#
#
#
def FIG_normalised_panels_timeline(gpta, output, field_data, fignum):
    # 5.
    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 4.5))
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    gpta.plot.scatter(x='Time', y='Averaged_Panels', title='All Panels', color='black', ax=axes)
    gpta.plot.line(x='Time', y='Averaged_Panels', ax=axes, style='b', legend=False)
    axes.set_ylabel("Average Panel Radiance")
    axes.set_xlabel("Time (seconds)")

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_TimevsAvgPanels.png')
