import folium
import pandas as pd
from flask import Flask, render_template
from folium.plugins import MarkerCluster
import geocoder

app = Flask(__name__)

@app.route('/')

def index():
    dataset = pd.read_csv('lab_coordinate.csv')
    place = dataset[ ['Latitude', 'Longitude'] ]
    place=place.values.tolist()

    my_location = geocoder.ip('me')

    df_text = dataset['Test Lab Name']

    xlat = dataset['Latitude'].tolist()
    xlon = dataset['Longitude'].tolist()
    locations = list(zip(xlat, xlon))
    map2 = folium.Map(location=my_location.latlng, tiles='CartoDB dark_matter', zoom_start=8)
    marker_cluster = MarkerCluster().add_to(map2)

    title_html = '''
    			<style>
	                .button3 {border-radius: 8px;}

	                .button {
	                  background-color: #4CAF50; /* Green */
	                  border: none;
	                  color: white;
	                  padding: 15px 32px;
	                  text-align: center;
	                  margin-left: 42%;
			  margin-bottom: 10px;
	                  text-decoration: none;
	                  display: inline-block;
	                  font-size: 16px;
	                }
                </style>
             	 <h3 align="center" style="font-size:20px"><b>Covid-19 Active Test Lab Near You</b></h3>
             	 <button class="button button3" onclick="location.href='http://127.0.0.1:5000/detail'">Detail Description</button>
             	 '''

    map2.get_root().html.add_child(folium.Element(title_html))

    folium.Marker(
                location=my_location.latlng, 
                popup='Me',
                icon=folium.Icon(color='darkblue', icon_color='white', icon='male', angle=0, prefix='fa')
            ).add_to(map2)

    try:
        for point in range(0, len(locations)):
            folium.Marker(locations[point], 
                          popup = folium.Popup(df_text[point]),
                         ).add_to(marker_cluster)    
    except:
        pass
    map2.save('map.html')

    return render_template('index.html')


@app.route("/detail/")
def detail():
    return render_template('detail.html')


if __name__ == '__main__':
   app.run(debug=True)
