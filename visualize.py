import psycopg2
import matplotlib.pyplot as plt
import folium
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def map_distances(connection):
    cursor = connection.cursor()


    select_matched = "SELECT nearest_street_pri, nearest_street_sec, latitude, longitude, address FROM addresses WHERE nearest_street_pri > 0;"

    cursor.execute(select_matched)

    streets_to_plot = []
    street_ids = []

    addresses = [list(x) for x in cursor.fetchall()]

    select_street_from_ids = "SELECT latitude, longitude FROM street_points WHERE street_id_primary = %s AND street_id_secondary = %s"


    colors = ['blue', 'red', 'green', 'orange', 'purple', 'pink', 'black', 'brown']
    print(len(addresses))

    m = folium.Map(location=[37.7749, -122.4194], zoom_start=10)


    for i, address in enumerate(addresses[:30]):
        #plot address
        lat = address[2]
        lon = address[3]
        #plt.scatter(address[2], address[3], color = 'red')
        folium.Marker([lat, lon], icon=folium.Icon(color='red')).add_to(m)


        print(address[0], address[1])
        cursor.execute(select_street_from_ids, (address[1], address[0]))
        street_coords = [list(x) for x in cursor.fetchall()]
        print(street_coords)

        if address[0] not in street_ids:
            for point in street_coords:
                #plt.scatter(point[0], point[1], color= 'blue')
                folium.Marker([point[0], point[1]], icon=folium.Icon(color='blue')).add_to(m)
            street_ids.append(address[0])


        #plt.show()
        m.save('map.html')





def prop_points(connection):

    cursor = connection.cursor()

    select_matched = "SELECT * FROM addresses WHERE latitude is not null and zip = 94102;"

    cursor.execute(select_matched)

    points = [list(x) for x in cursor.fetchall()]

    prop_locs_list = [
        [x[4], x[5], 'black', x[6], ",".join([str(y) for y in x[1:3]])] for x in points
    ]

    return prop_locs_list


def street_points():
    WEST_END = -122.4276
    EAST_END = -122.401686
    NORTH_END = 37.791812
    SOUTH_END = 37.77075
    streets = []
    with open('street_segments/segments.json', 'r') as file:
        streets = json.load(file)

    colors = [
        'red',
        'green',
        'blue',
        'yellow',
        'cyan',
        'magenta',
        'gray',
        'orange',
        'darkgreen',
        'purple'
    ]
    street_locs_list = []
    for i, item in enumerate(streets):

        for coor in streets[item]['coordinates']:
            lat = coor[0][0]
            lon = coor[0][1]
            if lon >= WEST_END or lon <= EAST_END or lat >= SOUTH_END or lat <= NORTH_END:
                row = [coor[0][0], coor[0][1], colors[i%10], streets[item]["name"], json.loads(streets[item]["segment_id"])]
                street_locs_list.append(row)
    
    return street_locs_list



def make_points(connection):

    prop_list = prop_points(connection)

    print(len(prop_list))

    street_list = street_points()

    street_list.extend(prop_list)

    street_df = pd.DataFrame(street_list, columns=[
                             'Lat', 'Lon', 'Color', 'Name', 'Ids'])

    fig = px.scatter_mapbox(street_df,
                            lat="Lat",
                            lon="Lon",
                            hover_name="Ids",
                            hover_data="Name",
                            zoom=12,
                            height=800,
                            width=800,
                            color="Color", 
                            color_discrete_sequence=['red',
                                                     'green',
                                                     'blue',
                                                     'yellow',
                                                     'cyan',
                                                     'magenta',
                                                     'gray',
                                                     'orange',
                                                     'darkgreen',
                                                     'purple',
                                                     'black'
                                                     ],)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.show()


if __name__ == "__main__":
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="unebarque3",
        database="sf_property_mapping"
    )
    #map_distances(connection)

    #map_streets()

    make_points(connection)

    #show_points(connection)

    connection.commit()
    connection.close()
