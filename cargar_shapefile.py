from osgeo import ogr
import os, re
import json
import zipfile
import time
import numpy as np

# from shapely.geometry.polygon import LinearRing, Polygon
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection


def open_shape(zippedfile="./HYS20120418.zip", decompressdir="./descomp"):
    zipf = zipfile.ZipFile(zippedfile)
    regexext = re.compile(".*\.shp$")
    nameshapes = list(filter(lambda x: regexext.match(x), zipf.namelist()))
    # print(nameshapes)
    os.makedirs(decompressdir, exist_ok=True)
    nameshapesp = list(map(lambda x: x.replace(".shp", ""), nameshapes))
    shapedict = dict()
    for shapef, shapename in zip(nameshapes, nameshapesp):
        zipf.extract(shapef, decompressdir)
        zipf.extract(shapef.replace(".shp", ".shx"), decompressdir)
        shapepath = os.path.join(decompressdir, shapef)
        # print(shapepath)
        shapefile = ogr.Open(shapepath)
        shapelayer = shapefile.GetLayer(0)
        nfeats = shapelayer.GetFeatureCount()
        coords = []
        values_f = []
        for i in range(nfeats):
            # first feature of the shapefile
            feature = shapelayer.GetFeature(i)
            jsonfeat = feature.ExportToJson()
            values = json.loads(jsonfeat)
            values_arr = values["geometry"]["coordinates"][0]
            values_f.append(values)
            # La primer capa es la mas grande, preguntar si se utilizaria
            coords.append(np.asarray(values_arr))
        shapedict.update({shapename: {"jsonShape": values_f,
                                      "coords": coords}})
    return shapedict


def graph_shape(coords):
    minx = np.min(list(map(lambda x: x[:, 0].min(), coords)))
    maxx = np.max(list(map(lambda x: x[:, 0].max(), coords)))
    miny = np.min(list(map(lambda x: x[:, 1].min(), coords)))
    maxy = np.max(list(map(lambda x: x[:, 1].max(), coords)))
    patches = []
    fig, ax = plt.subplots()
    for co in coords:
        polygon = Polygon(co, True)
        patches.append(polygon)
    p = PatchCollection(patches, cmap=plt.cm.jet, alpha=0.4)
    ax.add_collection(p)
    ax.set_xlim(minx - 1, maxx + 1)
    ax.set_ylim(miny - 1, maxy + 1)
    # fig.show()
    return fig, patches


def georef2pix(coords, metadata):
    """Traducir las coordenadas del poligono a pixeles en una imagen.
    Las coordenadas pertenecen a una imagen tipo shape, un poligono cerrado
    georeferenciado, mientras que los metadatos deben ser las descripciones del
    tamaño de la imagen y el paso asociado a cada pixel."""
    pass


def reubicar(array, magnitud, origen):
    minarr = array.min()
    origin = array - minarr
    maxarr = array.max()
    normal = (origin * magnitud / maxarr) + origen
    return normal


def poligon2bitmap(polygon, size=(300, 300), offset=30):
    polyx = reubicar(polygon[:, 0], size[0] - offset, offset)
    polyy = reubicar(polygon[:, 1], size[1] - offset, offset)
    img = np.zeros((size[0], size[0], 3), dtype=np.uint8)
    points = np.hstack((polyx.reshape(-1, 1), polyy.reshape(-1, 1)))
    # cv2.fillPoly(img, pts=[points], color=(255, 0, 0))
    return points
