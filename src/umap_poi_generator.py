#!/usr/bin/env python3

import requests
import sys
import json
import config
from functools import lru_cache

# Caching to avoid calling the API too much
@lru_cache
def geocoding(city):
    r = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city},,{config.COUNTRY}&limit=5&appid={config.API_KEY}')
    if r.status_code != 200:
        print(f'Err: bad status code from geocoding server ({r.status_code}).')
        exit(-1)
    result = r.json()
    if len(result) == 0:
        print(f'Warn: city {city} not found.')
        return None
    # For now, we only return the first occurrence.
    # Sometimes, the same city has two entries. :/
    # elif len(result) > 1:
    #     print(f'Warn: to much result for city {city}: { ', '.join([ x['name'] for x in result ]) }')
    else:
        return ( result[0]['lat'], result[0]['lon'] )
    return

# Arguments
if len(sys.argv) != 3:
    print(f'Syntax: {sys.argv[0]} <input.txt> <output.json>')
    exit(-1)
_, inputname, outputname = sys.argv

# Check the input file
try:
    data = open(inputname, 'rb').read().split(b'\n')
    data = [ x.decode().split(',') for x in data ]
    data = [ [ y.strip() for y in x ] for x in data ]
except Exception as e:
    print(f'Unable to read input: {e}. Abort !')
    exit(-1)

# Build a dict position => names
results = dict()
for name, city, area in data:
    coordinates = geocoding(city)
    if coordinates:
        position = ( coordinates[1], coordinates[0] )
        if position not in results:
            results[position] = list()
        results[position].append(name)

# Build the results
features = list()
for position, names in results.items():
    features.append( {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": position,
        },
        "properties": {
            "name": ', '.join(names),
        }
    } )

# Write the output
output = {
    "type": "FeatureCollection",
    "features": features
}
open(outputname, "w").write(json.dumps(output))