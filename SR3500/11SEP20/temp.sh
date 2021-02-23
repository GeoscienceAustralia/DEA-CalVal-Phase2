cd /g/data/up71/projects/CalVal_Phase1/brdf
source module_C5.sh
sed -i "40s/.*/        self.acquisition_datetime = dateutil.parser.parse('2018-05-20 02:16:38')/" retrieve_brdf_C5.py
sed -i "43s/.*/        bbox = geopandas.GeoDataFrame({'geometry': [box(115.155105, -30.585143333333335, 115.15636, -30.58394)]})/" retrieve_brdf_C5.py
python retrieve_brdf_C5.py > temp.txt ; awk -f format_Sent.awk temp.txt
