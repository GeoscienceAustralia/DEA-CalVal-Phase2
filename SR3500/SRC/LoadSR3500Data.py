from datetime import datetime, timedelta
import pandas as pd
import glob, os, subprocess


###############################################################################
#                                                                             #
# Action functions are defined to retrieve specific parts of the header for   #
# each spectrum. These functions are used in extract_metadata.                #
#                                                                             #
###############################################################################

# Date
def action1(l):
    return l[17:-1]

# Temperature (350-1000 temperature)
def action2(l):
    return l[17:]

# Battery Voltage
def action3(l):
    return l[17:]

# Integration time
def action4(l):
    return l[-3:-1]

# Latitude
def action5(l):
    return l

# Longitude
def action6(l):
    return l[10:-2]

# Time
def action7(l):
    return l[9:-1]

#
# Based on action functions defined above, extract header metadata from
# a file.
#
def extract_metadata(filename):
    strings = {
        'Date': action1,
        'Temperature': action2,
        'Voltage': action3,
        'Integration': action4,
        'Latitude': action5,
        'Longitude': action6,
        'GPS Time': action7
    }
    
    with open(filename) as file:
        list_of_actions = []
        for line in file:
            for search, action in strings.items():
                if search in line:
                    list_of_actions.append(action(line))

        return list_of_actions

#
### Extract spectrum and header information from a spectrum file. 
### Create a Pandas dataframe with the result.
#
def load_spectrum_to_df(infile, calfile):
    
    p1 = subprocess.Popen(["grep", "-an", "Data", infile], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["cut", "-d:", "-f", "1"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    fdl,err = p2.communicate()

    firstDataLine = int(fdl)

    date_str, tempstr, voltstr, int_time, lat, lon, time_str = extract_metadata(infile)
    
    date_time = date_str + time_str

    date_saved = datetime.strptime(date_str+time_str, '%m/%d/%Y %I:%M:%S %p')
    
    df = pd.read_csv(infile, skiprows=firstDataLine, sep='\t')
    if len(df.columns) == 3:
        df.columns = ['Wavelength', 'Rad_Ref', 'Rad_Target']
    else:
        df.columns = ['Wavelength', 'Rad_Target']

    df.Wavelength = df.Wavelength.round(3)
    #df.set_index('Wavelength', inplace=True)

    cal_data = pd.read_csv(calfile)
    cal_data.wl = cal_data.wl.round(3)
    cal_data.set_index('wl', inplace=True)
    cal_data.index.name = 'Wavelength'
    df['CalData'] = cal_data

    df['filename'] = infile.split("/")[-1:][0]
    df['date_saved'] = date_saved
    try:
        df['IntTime'] = float(int_time)
    except ValueError:
        df['IntTime'] = float(int_time[1:])
    df['Latitude'] = float(lat.split(' ')[1])
    df['Longitude'] = float(lon)

    temp1 = float(tempstr.split(',')[3])
    temp2 = float(tempstr.split(',')[4])
    temp3 = float(tempstr.split(',')[5])

    df['Temp1'] = temp1
    df['Temp2'] = temp2
    df['Temp3'] = temp3

    volt = float(voltstr.split(',')[1])
    df['Voltage'] = volt

    return df

#
### Loop through all spectrum files in "indir" and combine the resulting dataframes.
#
# For each 'line*' directory in 'indir', iterate through each file
# ending with 'suffix' and run 'load_spectrum_to_df'. Finally,
# return a concatenated dataframe made up of all the individual
# dataframes.
#
def load_from_dir(indir, calfile):
    all_dfs = []
    #
    # Initalise 'spectra' list and fill with files that end in 'suffix'
    #
    spectra = []
    for root, dirs, files in sorted(os.walk(indir)):
        for file in files:
            spectra.append(file)
    spectra = sorted(spectra)

    count=0
    for name in spectra:

        infile = indir + name
        
        df = load_spectrum_to_df(infile, calfile)
        df['Spec_number'] = count
        count +=1
        all_dfs.append(df)
    alldata = pd.concat(all_dfs)
    return alldata
