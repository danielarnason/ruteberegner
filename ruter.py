import requests
import pydawa
import pandas as pd
import json
from tqdm import tqdm
import re

base_url = 'http://10.65.130.183:5000/route/v1/foot/'

test_skolekoordinat = '12.30752919,55.73275526'

def read_data(filename):
    df = pd.read_csv(filename, sep=';', encoding='latin1')
    return df

def beregn_rute(fra, til):
    params = f'{fra};{til}?geometries=geojson&overview=full'
    url = base_url + params
    rute = requests.get(url).json()
    return rute

if __name__ == '__main__':
    data = read_data('export876867520626466480.csv')
    data = data.sample(n=300, random_state=42)

    routes = {
        'features': [],
        'type': 'FeatureCollection',
    }
    
    for idx, row in tqdm(data.iterrows()):

        vejnavn_re = re.search(r'^(\D*)\s|,', row['adresse1'])
        vejnavn = vejnavn_re.group(1)
        # vejnavn =  row['adresse1'].split(' ')[0]
        husnr = row['husnr']
        postnr = row['postnr']

        dawa_respons = pydawa.Adressesoeg(vejnavn, husnr, postnr, srid=4326).info()
        if len(dawa_respons) > 0:
            koordinater = str(dawa_respons[0]['x']) + ',' + str(dawa_respons[0]['y'])

            osrm_data = beregn_rute(koordinater, test_skolekoordinat)
            rute_geom = osrm_data['routes'][0]['geometry']
            feature = {
                'geometry': rute_geom,
                'id': idx,
                'properties': {},
                'type': 'Feature',
            }
            routes['features'].append(feature)

    with open('test.geojson', 'w') as output:
        json.dump(routes, output)
