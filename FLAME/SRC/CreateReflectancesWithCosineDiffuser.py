import numpy as np
import pandas as pd


#
#### Create dataframe with Reflectances based on measurements with separate
#### cosine diffuser for total downwelling
#
#Loop through each Line with spectral data:
#    1. Make an average of all the CosDiff spectra within the Line
#       (line_avg_panel).
#    2. For each ground spectrum within the Line, divide by the average CosDiff
#       spectrum (refl_temp).
#    3. Multiply each normalised ground spectrum by pi to create
#       reflectances dataframe (line_refls).
#
# Finally, combine each dataframe for reflectances within a line into a single
# dataframe (all_refls) 
#
def create_reflectances(good_panels, good_panel_spec, good_grounds_spec, field_data):

    if field_data[5] == 'Radiance':
        frames = []
        for j in good_panels.Line.unique():

            # 1.
            line_name_pans = [col for col in good_panel_spec.columns if 'radiance' in col]

            tmplist = []
            for i in line_name_pans:
                temp = good_panel_spec[i]
                tmplist.append(temp)

            #import ipdb
            #ipdb.set_trace()
            tmp_df = pd.concat(tmplist, axis=1)
            line_avg_panel = tmp_df.mean(axis=1)

            # 2.
            line_name_grounds = [col for col in good_grounds_spec.columns if 'radiance'+str(j)+'-' in col]

            tmplist = []
            for i in line_name_grounds:
                temp = good_grounds_spec[i]
                tmplist.append(temp)

            tmp_df = pd.concat(tmplist, axis=1)
            refl_tmp = tmp_df.div(line_avg_panel, axis=0)

            # 3.
            Factor = np.pi
            line_refls = pd.np.multiply(refl_tmp, Factor)

            frames.append(line_refls)

        return pd.concat(frames, axis=1)

    else:
        all_refls=0

    return all_refls
