from django.contrib.gis.geos import Point
from django.contrib.gis.gdal import OGRGeometry, SpatialReference

def transform_rd(point):
    ''' Please note this returns an OGRGeometry, not a point '''
    src_string = '+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +units=m +towgs84=565.2369,50.0087,465.658,-0.406857330322398,0.350732676542563,-1.8703473836068,4.0812 +no_defs no_defs <>'     
    src_srs = SpatialReference(src_string) 
    geom = OGRGeometry(point.wkt, src_srs) 
    geom.transform(4326)
    return geom