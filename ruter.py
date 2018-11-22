import requests
import pydawa
import pandas as pd

base_url = 'https://router.project-osrm.org/route/v1/foot/'

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
    data = data.sample(n=1, random_state=42)
    
    for idx, row in data.iterrows():

        vejnavn =  row['adresse1'].split(' ')[0]
        husnr = row['husnr']
        postnr = row['postnr']

        dawa_respons = pydawa.Adressesoeg(vejnavn, husnr, postnr, srid=4326).info()[0]
        koordinater = str(dawa_respons['x']) + ',' + str(dawa_respons['y'])

        rute = beregn_rute(koordinater, test_skolekoordinat)
        print(rute)