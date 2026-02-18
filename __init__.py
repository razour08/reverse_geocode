# -*- coding: utf-8 -*-

import csv, logging, os, sys, zipfile
if sys.platform == 'win32':
    csv.field_size_limit(2**31-1)
else:
    csv.field_size_limit(sys.maxsize)
try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve
from scipy.spatial import cKDTree as KDTree

# location of geocode data to download
GEOCODE_URL = 'http://download.geonames.org/export/dump/cities1000.zip'
GEOCODE_FILENAME = 'cities1000.txt'
ALTERNATE_NAMES_URL = 'http://download.geonames.org/export/dump/alternateNames.zip'
ALTERNATE_NAMES_FILENAME = 'alternateNames.txt'


def singleton(cls):
    """Singleton pattern to avoid loading class multiple times
    """
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class GeocodeData:

    def __init__(self, geocode_filename='geocode.csv', country_filename='countries.csv'):
        coordinates, self.__locations = self.__extract(rel_path(geocode_filename))
        self.__tree = KDTree(coordinates)
        self.__load_countries(rel_path(country_filename))

    def __load_countries(self, country_filename):
        """Load a map of country code to name
        """
        self.__countries = {}
        with open(country_filename, 'r') as handler:
            for code, name in csv.reader(handler):
                self.__countries[code] = name

    def query(self, coordinates):
        """Find closest match to this list of coordinates
        """
        try:
            distances, indices = self.__tree.query(coordinates, k=1)
        except ValueError as e:
            logging.info('Unable to parse coordinates: {}'.format(coordinates))
            raise e
        else:
            results = [self.__locations[index] for index in indices]
            for result in results:
                result['country'] = self.__countries.get(result['country_code'], '')
            return results

    def __download(self):
        """Download geocode file
        """
        for url in (GEOCODE_URL, ALTERNATE_NAMES_URL):
            local_filename = os.path.abspath(os.path.basename(url))
            if not os.path.exists(local_filename):
                logging.info('Downloading: {}'.format(url))
                urlretrieve(url, local_filename)
        return local_filename

    def __extract(self, local_filename):
        """Extract geocode data from zip
        """
        if os.path.exists(local_filename):
            # open compact CSV
            rows = csv.reader(open(local_filename, 'r', encoding='utf-8'))
        else:
            if not os.path.exists(GEOCODE_FILENAME) or not os.path.exists(ALTERNATE_NAMES_FILENAME):
                # remove files to get updated data
                if os.path.exists(GEOCODE_FILENAME):
                    os.remove(GEOCODE_FILENAME)
                if os.path.exists(ALTERNATE_NAMES_FILENAME):
                    os.remove(ALTERNATE_NAMES_FILENAME)

                for url, filename in ((GEOCODE_URL, GEOCODE_FILENAME), (ALTERNATE_NAMES_URL, ALTERNATE_NAMES_FILENAME)):
                    downloadedFile = os.path.abspath(os.path.basename(url)) # Re-derive local filename
                    if not os.path.exists(downloadedFile): # Check if already downloaded in __download loop? No, this is clearer.
                         downloadedFile = self.__download() # Wait, __download downloads BOTH now.

                    # Actually, let's simplify. __download ensures files are there.
                    # Just unzip them.
                    pass 

                # Re-do this logic properly.
                # 1. Download both if missing on extraction needed.
                self.__download()
                
                logging.info('Extracting: {}'.format(GEOCODE_FILENAME))
                with zipfile.ZipFile(os.path.abspath(os.path.basename(GEOCODE_URL))) as z:
                    with open(GEOCODE_FILENAME, 'wb') as fp:
                        fp.write(z.read(GEOCODE_FILENAME))

                logging.info('Extracting: {}'.format(ALTERNATE_NAMES_FILENAME))
                with zipfile.ZipFile(os.path.abspath(os.path.basename(ALTERNATE_NAMES_URL))) as z:
                    with open(ALTERNATE_NAMES_FILENAME, 'wb') as fp:
                        fp.write(z.read(ALTERNATE_NAMES_FILENAME))

            # Load Arabic names
            arabic_names = {}
            logging.info('Loading Arabic names...')
            with open(ALTERNATE_NAMES_FILENAME, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='\t')
                for row in reader:
                    # alternateNameId, geonameId, isolanguage, alternateName, isPreferred, isShort, isColloquial, isHistoric
                    if len(row) > 3 and row[2] == 'ar':
                         geoname_id = row[1]
                         arabic_name = row[3]
                         # Prefer short names or just overwrite? Let's just take the first one or overwrite.
                         # Maybe prefer if isPreferred? row[4]
                         arabic_names[geoname_id] = arabic_name

            # extract coordinates into more compact CSV for faster loading
            writer = csv.writer(open(local_filename, 'w', encoding='utf-8', newline=''))
            rows = []
            for row in csv.reader(open(GEOCODE_FILENAME, 'r', encoding='utf-8'), delimiter='\t'):
                geoname_id = row[0]
                latitude, longitude = row[4:6]
                country_code = row[8]
                if latitude and longitude and country_code:
                    city = row[1]
                    if geoname_id in arabic_names:
                        city = arabic_names[geoname_id]
                    
                    row = latitude, longitude, country_code, city
                    writer.writerow(row)
                    rows.append(row)
            
            # cleanup downloaded files? Maybe keep them for caching if user wants to rebuild.
            #Original code cleaned up. Let's keep it clean.
            for filename in (os.path.basename(GEOCODE_URL), os.path.basename(ALTERNATE_NAMES_URL), GEOCODE_FILENAME, ALTERNATE_NAMES_FILENAME):
                if os.path.exists(filename):
                     os.remove(filename)

        # load a list of known coordinates and corresponding __locations
        coordinates, __locations = [], []
        for latitude, longitude, country_code, city in rows:
            coordinates.append((latitude, longitude))
            __locations.append(dict(country_code=country_code, city=city))
        return coordinates, __locations


def rel_path(filename):
    """Return the path of this filename relative to the current script
    """
    return os.path.join(os.getcwd(), os.path.dirname(__file__), filename)


def get(coordinate):
    """Search for closest known location to this coordinate
    """
    gd = GeocodeData()
    return gd.query([coordinate])[0]


def search(coordinates):
    """Search for closest known locations to these coordinates
    """
    gd = GeocodeData()
    return gd.query(coordinates)


if __name__ == '__main__':
    # test some coordinate lookups
    city1 = -37.81, 144.96
    city2 = 31.76, 35.21
    print(get(city1))
    print(search([city1, city2]))
