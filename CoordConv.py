"""Contains the class to subset the selected area of the raster file."""
import numpy as np


class ConvCordinates:
    """Coordinates to slice array class."""

    def __init__(self, imag=None, geotrans=None, rastersize=None):
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
        """Get the image square limits in geocoords: LON and LAT."""
        coords = self.coords
        px = lambda x: coords['lono'] + coords['lonst'] * x
        py = lambda x: coords['lato'] + coords['latst'] * x
        limsx = [coords['lono'], px(coords['ncols'])]
        limsy = [coords['lato'], py(coords['nrows'])]
        return limsx, limsy
