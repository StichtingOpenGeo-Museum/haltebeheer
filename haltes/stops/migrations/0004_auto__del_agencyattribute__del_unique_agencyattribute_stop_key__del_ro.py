# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'AgencyAttribute', fields ['stop', 'key']
        db.delete_unique('stops_agencyattribute', ['stop_id', 'key'])

        # Deleting model 'AgencyAttribute'
        db.delete_table('stops_agencyattribute')

        # Deleting model 'RouteSegment'
        db.delete_table('stops_routesegment')

        # Adding model 'SourceAttribute'
        db.create_table('stops_sourceattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Source'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('stops', ['SourceAttribute'])

        # Adding unique constraint on 'SourceAttribute', fields ['stop', 'key']
        db.create_unique('stops_sourceattribute', ['stop_id', 'key'])

        # Adding model 'Source'
        db.create_table('stops_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_id', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('stops', ['Source'])

        # Adding model 'TripSegment'
        db.create_table('stops_tripsegment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Trip'])),
            ('from_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_stop', to=orm['stops.Stop'])),
            ('to_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_stop', to=orm['stops.Stop'])),
            ('line', self.gf('django.contrib.gis.db.models.fields.LineStringField')()),
        ))
        db.send_create_signal('stops', ['TripSegment'])

        # Adding model 'Trip'
        db.create_table('stops_trip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Route'])),
        ))
        db.send_create_signal('stops', ['Trip'])

        # Adding unique constraint on 'Stop', fields ['tpc']
        db.create_unique('stops_stop', ['tpc'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Stop', fields ['tpc']
        db.delete_unique('stops_stop', ['tpc'])

        # Removing unique constraint on 'SourceAttribute', fields ['stop', 'key']
        db.delete_unique('stops_sourceattribute', ['stop_id', 'key'])

        # Adding model 'AgencyAttribute'
        db.create_table('stops_agencyattribute', (
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Agency'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('stops', ['AgencyAttribute'])

        # Adding unique constraint on 'AgencyAttribute', fields ['stop', 'key']
        db.create_unique('stops_agencyattribute', ['stop_id', 'key'])

        # Adding model 'RouteSegment'
        db.create_table('stops_routesegment', (
            ('from_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_stop', to=orm['stops.Stop'])),
            ('to_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_stop', to=orm['stops.Stop'])),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Route'])),
            ('line', self.gf('django.contrib.gis.db.models.fields.LineStringField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('stops', ['RouteSegment'])

        # Deleting model 'SourceAttribute'
        db.delete_table('stops_sourceattribute')

        # Deleting model 'Source'
        db.delete_table('stops_source')

        # Deleting model 'TripSegment'
        db.delete_table('stops_tripsegment')

        # Deleting model 'Trip'
        db.delete_table('stops_trip')


    models = {
        'stops.agency': {
            'Meta': {'object_name': 'Agency'},
            'agency_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tz': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stops.route': {
            'Meta': {'object_name': 'Route'},
            'agencies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['stops.Agency']", 'symmetrical': 'False'}),
            'common_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'common_destination': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destination'", 'to': "orm['stops.Stop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'origin'", 'to': "orm['stops.Stop']"})
        },
        'stops.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'stops.sourceattribute': {
            'Meta': {'unique_together': "(('stop', 'key'),)", 'object_name': 'SourceAttribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Source']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Stop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'stops.stop': {
            'Meta': {'object_name': 'Stop'},
            'common_city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Stop']", 'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'stop_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'tpc': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        },
        'stops.stopattribute': {
            'Meta': {'unique_together': "(('stop', 'key'),)", 'object_name': 'StopAttribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Stop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'stops.trip': {
            'Meta': {'object_name': 'Trip'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Route']"}),
            'trip_id': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'stops.tripsegment': {
            'Meta': {'object_name': 'TripSegment'},
            'from_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_stop'", 'to': "orm['stops.Stop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'to_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_stop'", 'to': "orm['stops.Stop']"}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Trip']"})
        }
    }

    complete_apps = ['stops']
