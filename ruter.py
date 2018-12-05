import requests
import pydawa
import pandas as pd
import json
from tqdm import tqdm
import re

base_url = 'http://10.65.130.183:5000/route/v1/foot/'

def read_data(filename):
    df = pd.read_csv(filename, sep=';', encoding='latin1')
    return df

def beregn_rute(fra, til):
    params = f'{fra};{til}?geometries=geojson&overview=full'
    url = base_url + params
    rute = requests.get(url).json()
    return rute

def get_skole_pkt(vejnavn, husnr, postnr):
    adresse = pydawa.Adressesoeg(vejnavn, husnr, postnr, srid='4326').info()[0]
    koordinat = f'{adresse["x"]},{adresse["y"]}'
    return koordinat

if __name__ == '__main__':
    data = read_data('soeagerskolen.csv')
    skole_koordinat = get_skole_pkt('Flodvej', '89', '2765')

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

            osrm_data = beregn_rute(koordinater, skole_koordinat)
            rute_geom = osrm_data['routes'][0]['geometry']
            feature = {
                'geometry': rute_geom,
                'id': idx,
                'properties': {
                    'id': idx,
                    'distance': osrm_data['routes'][0]['distance'],
                    'duration': osrm_data['routes'][0]['duration'],
                    'klassetrin': row['klassetrin'],
                    # 'er_transportberettiget': row['er_transportberettiget']
                },
                'type': 'Feature',
            }
            routes['features'].append(feature)

    with open('soeagerskolen_boesagerskolen_ruter.geojson', 'w') as output:
        json.dump(routes, output)
