from fastapi import FastAPI
import uvicorn
from fastapi.responses import HTMLResponse
import pandas as pd 
import folium

#from map import Map
#from trend import Trend

# create the app as an instance of the fastAPI class
app = FastAPI()

# load the database once when the server starts

# create a root endpoint that provide basic information about the webapp

# I have lots of trouble to get my codes working recently. I put this up just for homework sake.
# percentage positive by modzcta 
percpos = "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/trends/percentpositive-by-modzcta.csv"
df_percpos = pd.read_csv(percpos, header = None)
# geoJson data
geo = "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/Geography-resources/MODZCTA_2010_WGS1984.geo.json"
# use the folium to generate the map 
# data cleanup for percentage postive 
df_percpos_clean = df_percpos.copy()
columnname = df_percpos[:1].values.flatten().tolist()
columnname = [i.replace('PCTPOS_','') for i in columnname if 'PCTPOS_' in i]
columnname.insert(0,'date')
df_percpos_clean.columns = columnname
df_percpos_clean = df_percpos_clean.drop(['CITY','BX','BK','MN','QN','SI'],axis=1)
df_percpos_clean = df_percpos_clean.tail(1).reset_index(drop=True)
df_percpos_clean = df_percpos_clean.T
date = df_percpos_clean.iloc[0,0]
df_percpos_clean = df_percpos_clean.iloc[1:]
df_percpos_clean = df_percpos_clean.reset_index()
df_percpos_clean.columns = ['modzcta','percpos']
df_percpos_clean['percpos'] = pd.to_numeric(df_percpos_clean['percpos'], errors='ignore')
m = folium.Map(location=[40.8, -73.9],tiles="cartodbpositron", zoom_start=10)
folium.Choropleth(
    geo_data=geo,
    name="choropleth",
    data=df_percpos_clean,
    columns=["modzcta", "percpos"],
    key_on="feature.properties.MODZCTA",
    fill_color="BuPu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Percentage positive (%)",
).add_to(m)
folium.LayerControl().add_to(m)



@app.get("/")
def root():
    return {"message": """Go to /map"""} 

@app.get("/map", response_class=HTMLResponse)
def map():
	return m._repr_html_()

# create another endpoint for displaying the trend graph
#@app.get("/trend")

# create another endpoint for displaying the map 
# Just try out 
# Codes will be more refined later 
# @app.get("/map/{data_type}", response_class=HTMLResponse)
# def map(data_type: str):
#	m = Map(data_type)
#	m = m.map()
# return m._repr_html_()
#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)
