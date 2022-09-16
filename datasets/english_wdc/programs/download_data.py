import requests
import os
from zipfile import ZipFile

ENGLISH_WDC_URL = """http://data.dws.informatik.uni-mannheim.de/largescaleproductcorpus/data/nonnormalizedOffers_english.json.gz"""


def download_file(url):
    local_filename = url.split('/')[-1]
    local_filename = os.path.join(os.path.dirname(__file__), "../data", local_filename)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            chunk_n = 0
            for chunk in r.iter_content(chunk_size=8192):
                chunk_n += 1
                if chunk_n % 1000 == 0:
                    print(f'Downloaded {chunk_n} 8KB chunks ({chunk_n * 8 / 1000} MB)')
                f.write(chunk)
    return local_filename


print('Downloading file\n')
local_filename = download_file(ENGLISH_WDC_URL)


print('Extracting downloaded file\n')
with ZipFile(local_filename, 'r') as zip:
    zip.printdir()
    zip.extractall(local_filename[:-3])


