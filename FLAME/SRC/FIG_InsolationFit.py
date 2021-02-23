import numpy as np
import matplotlib.pyplot as plt

from SRC.SolarAngle import solang
from scipy.stats import linregress


def FIG_insolation_fit(gpt, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    gpt['Solar_angle'] = gpt.apply(solang, axis=1)

    coszenith = np.cos(np.deg2rad(gpt['Solar_angle']))

    plt.plot(coszenith, gpt['Averaged_Panels'], color='blue')
    plt.scatter(coszenith, gpt['Averaged_Panels'], color='black')

    slope, intercept, r_value, p_value, std_err = linregress(coszenith, gpt['Averaged_Panels'])

    plt.plot(coszenith, slope*(coszenith)+intercept, color='red')
    plt.xlabel('Cos(Solar zenith angle)')
    plt.ylabel('Averaged panel radiance (W m$^{-2}$ nm$^{-1}$ sr$^{-1}$)')

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'Insolation.png')

    return slope, intercept, coszenith
