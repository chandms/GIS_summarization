import math
import sys
import json
import requests
from threading import Thread, activeCount
from time import sleep
import os

USAGE = """
        USAGE: fetcher.py ShallowLevel DeepestZoomLevel Lat Lon dirName
        """
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) +
                                (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def downloadThread(z, x, y):
    tileName = "%i-%i-%i.topojson" % (z, x, y)
    if(not os.path.isfile('tiles/' + tileName)):
        print("downloading", tileName)
        r = requests.get(
            "http://tile.mapzen.com/mapzen/vector/v1/all/%i/%i/%i.topojson?api_key=vector-tiles-HqUVidw" % (z, x, y))
        j = json.loads(r.text)
        j = json.dumps(j)
        # print(j)
        with open(dirName + '/' + tileName, 'w') as fd:
            fd.write(j)
            fd.close()
            print("downloaded", tileName)
    else:
        print("exists", tileName)


def downloader(currentZoom, maxZoom, x, y):
    if(maxZoom > currentZoom):
        downloader(currentZoom + 1, maxZoom, 2 * x, 2 * y)
        downloader(currentZoom + 1, maxZoom, (2 * x) + 1, 2 * y)
        downloader(currentZoom + 1, maxZoom, 2 * x, (2 * y) + 1)
        downloader(currentZoom + 1, maxZoom, (2 * x) + 1, (2 * y) + 1)
    while activeCount() > 50:
        sleep(1)
        pass
    t = Thread(target=downloadThread, args=(currentZoom, x, y))
    t.start()

if(len(sys.argv) < 5):
    print(USAGE)

else:
    lat = float(sys.argv[3])
    lon = float(sys.argv[4])
    Zoom1 = int(sys.argv[1])
    ZoomN = int(sys.argv[2])
    dirName = sys.argv[5]
    x, y = deg2num(lat, lon, Zoom1)
    downloader(Zoom1, ZoomN, x, y)
