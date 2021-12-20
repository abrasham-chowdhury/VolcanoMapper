import folium
import pandas
import http.server
import socketserver
import os

# Fetch data
data = pandas.read_csv("volcano_details.csv")
latitude = list(data["LAT"])
longitude = list(data["LON"])
elevation = list(data["ELEV"])
name = list(data["NAME"])


# Helpers
def set_marker_color(elevation_level):
    if elevation_level < 1000:
        return 'green'
    elif 1000 <= elevation_level < 3000:
        return 'orange'
    else:
        return 'red'


html = """
<h4>Volcano information</h4>
Name: <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a>
<br>Height: %s m<br>
"""

# Main
map1 = folium.Map(location=[38.58, -99.09], zoom_start=4, tiles='Stamen Terrain')
feature_group = folium.FeatureGroup(name="Volcano Map")

for lat, lon, elev, name in zip(latitude, longitude, elevation, name):

    iframe = folium.IFrame(html=html % (name, name, elev), width=200, height=100)

    feature_group.add_child(folium.Marker(location=[lat, lon],
                                          popup=folium.Popup(iframe),
                                          icon=folium.Icon(color=set_marker_color(elev))))

map1.add_child(feature_group)

map1.save("resources/volcano_map.html")

os.chdir(os.path.join(os.path.dirname(__file__), 'resources'))
socketserver.TCPServer(("", 3030), http.server.SimpleHTTPRequestHandler).serve_forever()
