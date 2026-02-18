# Reverse Geocode (Arabic Version)

[![Arabic](https://img.shields.io/badge/Language-Arabic-green)](README_AR.md)
[**اقرأ هذا الملف باللغة العربية**](README_AR.md)

Reverse Geocode takes a latitude / longitude coordinate and returns the nearest known country, state, and city in Arabic (where available).
This library is a fork of the original `reverse_geocode` library, customized to provide output in Arabic.

## Features
- **Offline Support**: Works completely offline with a local database.
- **Arabic Output**: Returns country and city names in Arabic.
- **Fast Lookup**: Uses a k-d tree for efficient nearest neighbour search.

This can be useful when you need to reverse geocode a large number of coordinates so a web API is not practical.

The geocoded locations are from [geonames](http://download.geonames.org/export/dump/). This data is then structured in to a [k-d tree](http://en.wikipedia.org/wiki/K-d_tree>) for efficiently finding the nearest neighbour. 

Note that as this is point based and not a polygon based lookup it will only give a rough idea of the location/city.


## Example usage

Example reverse geocoding a coordinate:

```
>>> import reverse_geocode
>>> melbourne_coord = -37.81, 144.96
>>> reverse_geocode.get(melbourne_coord)
{'country_code': 'AU', 'city': 'ملبورن', 'latitude': -37.814, 'longitude': 144.96332, 'population': 4917750, 'state': 'Victoria', 'country': 'أستراليا'}
```

Example reverse geocoding a list of coordinates:
```
>>> nyc_coord = 40.71427000, -74.00597000
>>> reverse_geocode.search((melbourne_coord, nyc_coord))
[{'country_code': 'AU', 'city': 'ملبورن', 'latitude': -37.814, 'longitude': 144.96332, 'population': 4917750, 'state': 'Victoria', 'country': 'أستراليا'},
 {'country_code': 'US', 'city': 'نيويورك', 'latitude': 40.71427, 'longitude': -74.00597, 'population': 8804190, 'state': 'New York', 'country': 'الولايات المتحدة'}]
```

By default the nearest known location is returned, which may not be as expected when there is a much larger city nearby.
For example querying for the following coordinate near NYC will return Seaport:

```
>>> nyc_coordinate = 40.71, -74.00
>>> reverse_geocode.get(nyc_coordinate)
{'country_code': 'US', 'city': 'Seaport', 'latitude': 40.70906, 'longitude': -74.00317, 'population': 8385, 'state': 'New York', 'county': 'New York County', 'country': 'United States'}
```

To filter for larger cities a minimum population can be set. Using a minimum population of `100000` with the above coordinate now returns NYC:
        
```
>>> reverse_geocode.get(nyc_coordinate, min_population=100000)
{'country_code': 'US', 'city': 'New York City', 'latitude': 40.71427, 'longitude': -74.00597, 'population': 8804190, 'state': 'New York', 'country': 'United States'}
```



## Offline Usage and Local Database

This library is designed to work completely offline after the initial setup.

### How it works:
1. **Raw Data**: The library relies on data files from [GeoNames](http://download.geonames.org/export/dump/):
   - `cities1000.zip`: Contains city information.
   - `alternateNames.zip`: Contains alternate names (including Arabic).

2. **Local Database**: When run for the first time, the library extracts these files and creates a compact, fast-loading local file named `geocode.gz` in the library directory. This file serves as the "local database".

### First Run:
- **With Internet**: The library will automatically download the required files (`cities1000.zip` and `alternateNames.zip`) and generate `geocode.gz`.
- **Without Internet (Manual)**:
  1. Download the following two files from an internet-connected machine:
     - [http://download.geonames.org/export/dump/cities1000.zip](http://download.geonames.org/export/dump/cities1000.zip)
     - [http://download.geonames.org/export/dump/alternateNames.zip](http://download.geonames.org/export/dump/alternateNames.zip)
  2. Place these two files in the project's root directory (or current working directory).
  3. When you run the code for the first time, the library will detect these files and generate `geocode.gz` from them without needing an internet connection.

Once `geocode.gz` is created, the zip files and internet connection are no longer needed. You can move `geocode.gz` along with your code to any other machine and it will work immediately.

## Install

```
pip install reverse-geocode
```
