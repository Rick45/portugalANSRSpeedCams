import json
import gpxpy
import gpxpy.gpx
import sys
from datetime import datetime


# Carregar a string do arquivo
#filetoLoad= "markers.txt"

import requests
onlineMode = True
if onlineMode:
    url = "https://radaresavista.pt/wp-content/themes/ansr-radares/data.json"
    response = requests.get(url)

    if response.status_code == 200:
        # Extract the filename from the URL
        filename = url.split("/")[-1].split("?")[0]

        # Save the content of the response to a file
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"File '{filename}' downloaded successfully.")
    else:
        print("Failed to download the file.")
        sys.exit(1)

json_file_path = "data.json"
# Open the JSON file
with open(json_file_path, "r", encoding="utf8") as json_file:
    # Parse the JSON data
    data = json.load(json_file)


'''
Sample Json
{
        "Estrada": "EN234",
        "Concelho": "Viseu",
        "Freguesia": "Nelas",
        "Km Inicial": 88.672,
        "Coordenada": "40.515384, -7.887122",
        "Km Final": "_",
        "Tipo": "VI",
        "EGV": "Infraestruturas de Portugal",
        "Sentido": "dois sentidos",
        "Velocidade": 70,
        "Fase": 2
}
'''
print("data size:", len(data))

# Get the current date
current_date = datetime.now()
# Format the date as "yyyymmdd"

formatted_date = current_date.strftime("%Y%m%d")
gpx = gpxpy.gpx.GPX()

gpx.name = 'Radares ANSR'+formatted_date
gpx.creator='Rick45'
gpx.author_link='https://github.com/Rick45/portugalANSRSpeedCams'
gpx.author_name='Ricardo'
gpx.creator='Ricardo'
gpx.description='Portugal Speed Cameras List'

for item in data:
    coordinatesString = item["Coordenada"]
    coordinatesString_trimmed = coordinatesString.replace(" ", "").replace("°", "")
    latitude, longitude = map(float, coordinatesString_trimmed.split(','))
    gpx_waypoint = gpxpy.gpx.GPXWaypoint(latitude, longitude)
    gpx_waypoint.name = f"{item['Tipo']} {item['Velocidade']} - {item['Estrada']} Km {item['Km Inicial']}"
    gpx_waypoint.description = f"Concelho: {item['Concelho']}, Tipo: {item['Tipo']}, Velocidade: {item['Velocidade']}"
    
    # You can add more information to the GPX waypoint as needed
    
    gpx.waypoints.append(gpx_waypoint)

gpx_str = gpx.to_xml()


fileNameToSave = 'Radares_ANSR'+formatted_date
with open(fileNameToSave+".gpx", "w") as f:
    f.write(gpx_str)

print("GPX file saved as "+fileNameToSave)