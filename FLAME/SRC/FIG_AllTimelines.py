import matplotlib.pyplot as plt


#
## Figure 
#
### Plot timelines for ALL panel and ground data, with one line in one panel
#
def FIG_all_timelines(gpta, adta, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(8.5, 3.5))
    plt.tight_layout(pad=1.5, w_pad=0.0, h_pad=0.0)

    gpta.plot(x='Time', y='ones', kind='scatter', legend=False, ax=axes, color='orange', marker='|', s=50, linewidth=0.8)
    adta.plot(x='Time', y='ones', kind='scatter', legend=False, ax=axes, marker='x', sharey=True, s=50, linewidth=0.8)
    axes.tick_params(axis='both', which='major', labelsize=9)
    axes.tick_params(axis='both', which='minor', labelsize=9)
    axes.set_xlabel("Time (seconds)")
    axes.set_ylabel("")
    axes.set_yticks([])

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_AllTimeLineData.png', dpi=300)
