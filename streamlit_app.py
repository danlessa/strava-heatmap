import streamlit as st

                
with st.sidebar:
    (slope_min, slope_max) = st.slider('Slope Min/Max', 0, 50, (0, 30))
    (density_min, density_max) = st.slider('Pop Density Min/Max', 0, 5000, (0, 1000))
    (elevation_min, elevation_max) = st.slider('Elevation Min/Max', 0, 5000, (600, 1300))


    slope_opacity = st.slider('Slope Opacity', 0.0, 1.0, 0.5)
    density_opacity = st.slider('Pop Density Opacity', 0.0, 1.0, 0.0)
    elevation_opacity = st.slider('Elevation Opacity', 0.0, 1.0, 0.5)
    heatmap_opacity = st.slider('Heatmap Opacity', 0.0, 1.0, 0.5)

    color = st.selectbox('Heatmap Color', ['blue', 'bluered', 'purple', 'hot', 'gray'])

import ee
ee.Initialize()

density_vis = {"max":density_max,"palette":["ffffe7","FFc869","ffac1d","e17735","f2552c","9f0c21"],"min":density_min, "opacity": 1.0}
slope_vis = {"min":slope_min,"max":slope_max, "opacity": 1.0}
elevation_vis = {"min":elevation_min,"max":elevation_max,"palette":["0000ff","00ffff","ffff00","ff0000","ffffff"], "opacity": 1.0}

dataset = ee.ImageCollection("CIESIN/GPWv411/GPW_UNWPP-Adjusted_Population_Density").first();
raster = dataset.select('unwpp-adjusted_population_density');


dsm_dataset = ee.ImageCollection("JAXA/ALOS/AW3D30/V3_2")
elevation = dsm_dataset.select('DSM')

# // Reproject an image mosaic using a projection from one of the image tiles,
# // rather than using the default projection returned by .mosaic().
proj = elevation.first().select(0).projection();
slopeReprojected = ee.Terrain.slope(elevation.mosaic()
                             .setDefaultProjection(proj));     



# url = 'https://heatmap-external-b.strava.com/tiles-auth/all/{color}/{z}/{x}/{y}.png?Key-Pair-Id={kpi}&Policy={policy}&Signature={signature}'
# DEFS = {'color': color, 'kpi': None, 'policy': None, 'signature': None}'
# url = url.format(**DEFS)

url = 'https://heatmap-external-b.strava.com/tiles/all/{color}'.format(color=color)

url += '/{z}/{x}/{y}.png?px=256'



import geemap.foliumap as geemap
import folium
Map = geemap.Map(center=(-23.5, -46.6), zoom=10)
Map.setOptions("SATELLITE")
Map.addLayer(raster, density_vis, 'unwpp-adjusted_population_density', False, density_opacity)
Map.addLayer(elevation, elevation_vis, 'Elevation', True, elevation_opacity)                                   
Map.addLayer(slopeReprojected, slope_vis, 'Slope', True, slope_opacity);
Map.add_tile_layer(url, name='Strava Heatmap', opacity=heatmap_opacity)
print('--------------------------')

# component_args = {
#     'handle_map_click': False,
#     'handle'
# }

Map.to_streamlit(width=2000, height=1000, bidirectional=True, responsive=True)