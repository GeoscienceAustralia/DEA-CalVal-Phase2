import os, stat, subprocess


def print_brdf(alldata, field_data):

    #
    # Look for Collection Upgrade version in field_data
    # Should be like 'C5' or 'C6'. If it doesn't exist, set it to 'C5'.
    #
    try:
        CNum = field_data[7]
    except IndexError:
        CNum = 'C5'
    
    UniqStr = field_data[0]+field_data[1]+field_data[2]+field_data[3]

    with open(UniqStr+'tempfile.sh', 'w') as tempfile:
        tempfile.write("#! /bin/bash\n")
        tempfile.write("cd /g/data/up71/projects/CalVal_Phase1/brdf\n")
        tempfile.write("source module_")
        tempfile.write(CNum)
        tempfile.write(".sh\n")
        tempfile.write("sed -i \"40s/.*/        self.acquisition_datetime = dateutil.parser.parse(\'")
        tempfile.write(str(alldata['date_saved'].iloc[0]))
        tempfile.write("')/\" retrieve_brdf_")
        tempfile.write(CNum)
        tempfile.write(".py\n")
        tempfile.write("sed -i \"43s/.*/        bbox = geopandas.GeoDataFrame({'geometry': [box(")
        tempfile.write(str(alldata['Longitude'].min()))
        tempfile.write(", ")
        tempfile.write(str(alldata['Latitude'].min()))
        tempfile.write(", ")
        tempfile.write(str(alldata['Longitude'].max()))
        tempfile.write(", ")
        tempfile.write(str(alldata['Latitude'].max()))
        tempfile.write(")]})/\" retrieve_brdf_")
        tempfile.write(CNum)
        tempfile.write(".py\n")
        tempfile.write("python retrieve_brdf_")
        tempfile.write(CNum)
        tempfile.write(".py > "+UniqStr+"temp.txt ; awk -f format_Sent.awk "+UniqStr+"temp.txt > "+UniqStr+"temp2.txt\n")

    os.chmod(UniqStr+'tempfile.sh', stat.S_IRWXU)
    
    proc = subprocess.Popen(["./"+UniqStr+"tempfile.sh"], stdout = subprocess.PIPE)
    proc.communicate()

    import pandas as pd

    output = pd.read_csv('/g/data/up71/projects/CalVal_Phase1/brdf/'+UniqStr+'temp2.txt', index_col=0, sep=' ')

    # Cleanup
    os.remove(UniqStr+'tempfile.sh')
    os.remove('/g/data/up71/projects/CalVal_Phase1/brdf/'+UniqStr+'temp.txt')
    os.remove('/g/data/up71/projects/CalVal_Phase1/brdf/'+UniqStr+'temp2.txt')
    
    return output
