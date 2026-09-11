# Umap Point Of Interest

## Objectives

Python script allowing to generate a GEOJSON file with PoI from a list of labels and towns.

For instance, with an input file like this:

```
Label1, Paris
Label2, Lyon
Label3, Marseille
```

The script geocodes the location and generate a file that can be imported, for instance on [uMap](https://umap-project.org/).

## How to use it

Install the requirements:

```
python3 -m pip install -r requirements.txt
```

Creates `src/config.py` from `src/config.py.template` and adapt with an OpenWeatherMap API_KEY. See [here](https://openweathermap.org/price) for a free key.

Then launch the script:

```
Syntax: umap_poi_generator.py <input.txt> <output.json>
```