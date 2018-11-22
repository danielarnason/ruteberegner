import requests
import pydawa

base_url = 'http://10.65.130.183:5000/route/v1/foot/'

url_params = '12.15509,55.79567;12.36066,55.80858?geometries=geojson&overview=full'

url = base_url + url_params

r = requests.get(url)

r_json = r.json()

print(r_json)