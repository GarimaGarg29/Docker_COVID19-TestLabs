# Docker_Covid
A WebApp build using flask on platform Docker. This app will generate a map in which all the covid-19 test labs in india are marked.
## Quick Start

* Go to your project directory
* Create a `Dockerfile` with:

```Dockerfile
FROM python:3.7-alpine
WORKDIR /project
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
COPY index.html .
CMD ["flask", "run"]
```

* Create an `app` directory and enter in it
* Create a `app.py` file (it should be named like that and should be in your `app` directory) with:

```python
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
             	 <h3 align="center" style="font-size:20px"><b>Covid-19 Active Test Lab Near You</b></h3>
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

    return map2._repr_html_()


if __name__ == '__main__':
   app.run(debug=True)
```

the main application object should be named `app` (in the code) as in this example.

* Go to the project directory (in where your `Dockerfile` is, containing your `app` directory)
* Build your image:

```bash
docker build --tag flask-docker-demo-app .
```

* Run a container based on your image:

```bash
docker run --name flask-docker-demo-app -p 5001:5001 flask-docker-demo-app
```

...and you have an optimized Flask server in a Docker container.

You should be able to check it in your Docker container's URL, for example: <a href="http://192.168.99.100:5001" target="_blank">http://192.168.99.100:5001</a> or <a href="http://127.0.0.1:5000" target="_blank">http://127.0.0.1:5000</a>

<img src='https://raw.githubusercontent.com/shivam1808/Docker_Covid_Map/master/pic1.PNG' border='0' alt='Covid Map'/>
<img src='https://raw.githubusercontent.com/shivam1808/Docker_Covid_Map/master/pic2.PNG' border='0' alt='Covid Map'/>

<img src='https://raw.githubusercontent.com/shivam1808/Docker_Covid_Map/master/pic3.PNG' border='0' alt='Covid Map'/>
<img src='https://raw.githubusercontent.com/shivam1808/Docker_Covid_Map/master/pic4.PNG' border='0' alt='Covid Map'/>
