''' Imported from...'''
from django.contrib.gis.db.models.fields import GeometryField
from django.utils import simplejson
from django.http import HttpResponse

def render_to_geojson(query_set, geom_field=None, mimetype='text/plain', pretty_print=True, exclude=[]):
    '''
    
    Shortcut to render a GeoJson FeatureCollection from a Django QuerySet.
    Currently computes a bbox and adds a crs member as a sr.org link
    
    '''
    collection = {}

    # Find the geometry field
    # qs.query._geo_field()

    fields = query_set.model._meta.fields
    geo_fields = [f for f in fields if isinstance(f, GeometryField)]
    
    #attempt to assign geom_field that was passed in
    if geom_field:
        geo_fieldnames = [x.name for x in geo_fields]
        try:
            geo_field = geo_fields[geo_fieldnames.index(geom_field)]
        except:
            raise Exception('%s is not a valid geometry on this model' % geom_field)
    else:
        geo_field = geo_fields[0] # no support yet for multiple geometry fields

    #remove other geom fields from showing up in attributes    
    if len(geo_fields) > 1:
        for gf in geo_fields:
            if gf.name not in exclude: exclude.append(gf.name)
        exclude.remove(geo_field.name) 
        
    # Gather the projection information
    crs = {}
    crs['type'] = "link"
    crs_properties = {}
    crs_properties['href'] = 'http://spatialreference.org/ref/epsg/%s/' % geo_field.srid
    crs_properties['type'] = 'proj4'
    crs['properties'] = crs_properties 
    collection['crs'] = crs
    
    # Build list of features
    features = []
    if query_set:
        for item in query_set:
            feat = {}
            feat['type'] = 'Feature'
            d= item.__dict__.copy()
            g = getattr(item,geo_field.name)
            d.pop(geo_field.name)
            for field in exclude:
                d.pop(field)
            feat['geometry'] = simplejson.loads(g.geojson)
            feat['properties'] = d
            features.append(feat)
    else:
        pass #features.append({'type':'Feature','geometry': {},'properties':{}})

    # Label as FeatureCollection and add Features
    collection['type'] = "FeatureCollection"    
    collection['features'] = features
    
    # Attach extent of all features
    #if query_set:
    #    #collection['bbox'] = [x for x in query_set.extent()]
    #    agg = query_set.unionagg()
    #    collection['bbox'] = [agg.extent]
    #    collection['centroid'] = [agg.point_on_surface.x,agg.point_on_surface.y]
      
    # Return response
    response = HttpResponse()
    if pretty_print:
        response.write('%s' % simplejson.dumps(collection, indent=1))
    else:
        response.write('%s' % simplejson.dumps(collection))    
    response['Content-length'] = str(len(response.content))
    response['Content-Type'] = mimetype
    return response