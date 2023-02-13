"""Contains the class to subset the selected area of the raster file."""
import numpy as np
<<<<<<< HEAD
from osgeo import gdal
=======
>>>>>>> 5ff2f64d2f2293fc5bc0975e5d88687fdaa2fd59


class ConvCordinates:
    """Coordinates to slice array class."""

<<<<<<< HEAD
    def __init__(self, imag):
=======
    def __init__(self, imag=None, geotrans=None, rastersize=None):
>>>>>>> 5ff2f64d2f2293fc5bc0975e5d88687fdaa2fd59
        """Create the dictionary.

        Dictionary longitude and latitude origin and step in image.
        From the official site:
        --------------------------------------------------------------
        Xp = padfTransform[0] + P*padfTransform[1] + L*padfTransform[2]
        Yp = padfTransform[3] + P*padfTransform[4] + L*padfTransform[5]
        where P is for pixel and L for line
        --------------------------------------------------------------

        Parameters
        imag : gdal image object.
        """
<<<<<<< HEAD
        coordsval = np.asarray(imag.GetGeoTransform())
        coords = dict(lono=coordsval[0], lato=coordsval[3],
                      lonst=coordsval[1], latst=coordsval[5])
        coords.update(dict(ncols=imag.RasterXSize,
                           nrows=imag.RasterYSize))
        self.coords = coords

    def calcmatlims(self, coordd, cols=True):
=======
        if imag == None:
            assert geotrans is not None, "No hay informacion de entrada"
            coordsval = np.asarray(geotrans)
            rastersizex, rastersizey = rastersize
        else:
            coordsval = np.asarray(imag.GetGeoTransform())
            rastersizex, rastersizey = imag.RasterXSize, imag.RasterYSize
        coords = dict(lono=coordsval[0], lato=coordsval[3],
                      lonst=coordsval[1], latst=coordsval[5],
                      ncols=rastersizex, nrows=rastersizey)
        setattr(self, "coords", coords)

    def calcmatlims(self, coordlist):
>>>>>>> 5ff2f64d2f2293fc5bc0975e5d88687fdaa2fd59
        """Transform coordinates longitude or latitude to pixel values
        inside the pixel limits.

        Parameters
        ----------------------------------------------------
        coordd : dictionary with the coordinates points asked to
                 transform to pixels.
        cols : boolean, True for columns by default.
        output
        ----------------------------------------------------
        limsarr : dictionary with the limit pixels correspondant to
                  the geo coordinates in image.
        """
        coords = self.coords
<<<<<<< HEAD
        if cols:
            ncols = (coordd['lons'] - coordd['lono']) / coords['lonst']
            inicol = (coordd['lono'] - coords['lono']) / coords['lonst']
            limsarr = dict(inicol=int(inicol), endcol=int(inicol + ncols))
        else:
            nrows = (coordd['lats'] - coordd['lato']) / coords['latst']
            inirow = (coordd['lato'] - coords['lato']) / coords['latst']
            limsarr = dict(inirow=int(inirow), endrow=int(inirow + nrows))
        return limsarr

    def coords2pixels(self, band, coordlist):
        """Transform coordinates to pixel index and return array.

        Parameters
        __________
        coordict : coord dictionary with the innitial-final
                   latitude, and longitude
        band : Raster band to analyse

        Returns
        __________
        numpy array with data band.
        """
        labels = ['lono', 'lons', 'lato', 'lats']
        cdict = dict(zip(labels, coordlist))
        array = band.ReadAsArray()  # esto es innecesario
        rows = self.calcmatlims(cdict, False)
        cols = self.calcmatlims(cdict)
        return array, rows, cols

    def locationpoint(self, band, limits, point, slicmark=False):
        """Get the point over the subset array from longitude and latitude."""
        coords = self.coords
        pixx = (point[0] - coords['lono']) / coords['lonst']
        pixy = (point[1] - coords['lato']) / coords['latst']
        roundp = lambda x: int(np.floor(x + 0.5))
        pixx, pixy = roundp(pixx), roundp(pixy)
        array, ro, co = self.coords2pixels(band, limits)
=======
        # if cols:
        labels = ['lono', 'lons', 'lato', 'lats']
        cdict = dict(zip(labels, coordlist))
        inicol = (cdict['lono'] - coords['lono']) / coords['lonst']
        inirow = (cdict['lato'] - coords['lato']) / coords['latst']
        ncols = (cdict['lons'] - cdict['lono']) / coords['lonst']
        nrows = (cdict['lats'] - cdict['lato']) / coords['latst']
        limsarr = (dict(inirow=int(inirow), endrow=int(inirow + nrows)),
                   dict(inicol=int(inicol), endcol=int(inicol + ncols)))
        return limsarr


    def locationpoint(self, band, limits, point, slicmark=False):
        """Get the point in pixel index inside the subset defined with LON & LAT.
        Parameters
        ----------------------------------------------------
        band
        limits
        point
        slicmark
        """
        coords = self.coords
        pixx = (point[0] - coords['lono']) / coords['lonst']
        pixy = (point[1] - coords['lato']) / coords['latst']
        array = band.readAsArray()
        ro, co = self.calcmatlims(limits)
>>>>>>> 5ff2f64d2f2293fc5bc0975e5d88687fdaa2fd59
        sliced = array[ro['inirow']:ro['endrow'],
                       co['inicol']:co['endcol']]
        if slicmark:
            pixx = pixx - co['inicol']
            pixy = pixy - ro['inirow']
        return pixx, pixy, sliced, array

    ## Se necesita una función que calcule cada coordenada a pixel dentro de la
    ## imagen y regrese un arreglo que pueda ser utilizado como un polígono
    ## dentro de la imagen

    def band_limits(self):
<<<<<<< HEAD
        """Get the image square limits."""
=======
        """Get the image square limits in geocoords: LON and LAT."""
>>>>>>> 5ff2f64d2f2293fc5bc0975e5d88687fdaa2fd59
        coords = self.coords
        px = lambda x: coords['lono'] + coords['lonst'] * x
        py = lambda x: coords['lato'] + coords['latst'] * x
        limsx = [coords['lono'], px(coords['ncols'])]
        limsy = [coords['lato'], py(coords['nrows'])]
        return limsx, limsy
<<<<<<< HEAD


if __name__ == "__main__":
    imag = gdal.Open("../MAPA_AEROVIAS_GEORECTIFICADO2.tif",
                     gdal.gdal.GA_ReadOnly)
    cconv = ConvCordinates(imag)
=======
>>>>>>> 5ff2f64d2f2293fc5bc0975e5d88687fdaa2fd59
