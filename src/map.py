import json

import folium
import numpy as np
from PIL import Image
from folium import Marker, PolyLine
from folium.plugins import MarkerCluster

partner_locations = {
    'ThinkTac': [(13.005467936628618, 77.56458995073768),
                 (29.20709322879447, 76.03155180674312),
                 (30.317374801847905, 78.02841870949568)],
    'Mantra': [(12.906123320580075, 77.58367301536951),
               (12.71009033568906, 77.69852299006696),
               (25.62254493868842, 85.0901721210514)],
    'Eduweave': [(22.559234392562644, 88.3007281018251),
                 (22.34601070554623, 82.78559139727103)],
    'ORF': [(20.29414324246968, 85.80133845961052)]
}

partner_logos = {
    'ThinkTac': '/Users/sudeep/Documents/Code/sg-partner-dashboard/icons/thinktac.png',
    'Mantra': '/Users/sudeep/Documents/Code/sg-partner-dashboard/icons/mantra.png',
    'Eduweave': '/Users/sudeep/Documents/Code/sg-partner-dashboard/icons/eduweave.jpeg',
    'ORF': '/Users/sudeep/Documents/Code/sg-partner-dashboard/icons/orf.png'

}


def popup_html(partner_name, partner_url):

    left_col_color = '#19a7bd'
    right_col_color = '#f2f0d3'

    html = """<!DOCTYPE html>
    <html>
    <head>
    <h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(partner_name) + """
    </head>
        <table style="height: 126px; width: 350px;">
    <tbody>
    <tr>
    <td style="background-color: """ + left_col_color + """;"><span style="color: #ffffff;">Website</span></td>
    <td style="width: 150px;background-color: """ + right_col_color + """;">{}</td>""".format(partner_url) + """
    </tr>
    </tbody>
</table>
</html>
"""
    return html


def create_curve_points(
        start_lat_lon: tuple, end_lat_lon: tuple, control_point_position=0.5, control_point_offset=0.5, points=100
) -> list:
    # Function to calculate intermediate points along the Bezier curve
    def bezier_curve(p0, p1, p2, n_points=100):
        t = np.linspace(0, 1, n_points)
        points = np.zeros((len(t), 2))
        for i, _t in enumerate(t):
            points[i] = (1 - _t) ** 2 * p0 + 2 * (1 - _t) * _t * p1 + _t ** 2 * p2
        return points.tolist()

    start_lat_lon = np.array(start_lat_lon)
    end_lat_lon = np.array(end_lat_lon)

    # Calculate direction vector from End to Start
    direction_vector = end_lat_lon - start_lat_lon

    # Create control point that would be the pount where curliness occures
    control_point = start_lat_lon + direction_vector * control_point_position

    # Determine offset direction based on the offset factor
    if control_point_offset > 0:
        control_point += np.array([-direction_vector[1], direction_vector[0]]) * control_point_offset
    else:
        control_point += np.array([direction_vector[1], -direction_vector[0]]) * abs(control_point_offset)

    # Creating Bezier curve points
    curve_points = bezier_curve(start_lat_lon, control_point, end_lat_lon, points)
    return curve_points


with open('indiamap.json', 'r') as f:
    map_data = json.load(f)
india_map = folium.Map(location=[23, 82.3], tiles='esriworldgraycanvas', zoom_start=5)

marker_cluster = MarkerCluster()
for partner in partner_locations:
    icon = Image.open(partner_logos[partner])
    w, h = icon.size
    w = int(w / h * 30)
    h = 30
    hub_location = partner_locations[partner][0]
    for loc in partner_locations[partner]:
        icon = folium.features.CustomIcon(partner_logos[partner], icon_size=(w, h))
        if loc != hub_location:
            PolyLine(locations=create_curve_points(hub_location, loc), color='purple', weight=0.5, dashArray='0 4 0').add_to(india_map)
        popup = folium.Popup(folium.Html(popup_html(partner, partner), script=True), max_width=500)
        marker_cluster.add_child(Marker([loc[0], loc[1]], icon=icon, popup=popup))
india_map.add_child(marker_cluster)
folium.GeoJson(map_data,
               style_function=lambda x: {
                   'fillColor': '#372A8C',
                   'fillOpacity': 0.2,
                   'weight': 0.4,
                   'stroke': '#F2F2F2'
               }).add_to(india_map)
folium.LayerControl().add_to(india_map)

if __name__ == '__main__':
    india_map.show_in_browser()
