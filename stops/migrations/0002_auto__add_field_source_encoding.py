# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Source.encoding'
        db.add_column('stops_source', 'encoding', self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Source.encoding'
        db.delete_column('stops_source', 'encoding')


    models = {
        'stops.agency': {
            'Meta': {'object_name': 'Agency'},
            'agency_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tz': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stops.basestop': {
            'Meta': {'object_name': 'BaseStop'},
            'common_city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stop_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'stops.route': {
            'Meta': {'object_name': 'Route'},
            'agencies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['stops.Agency']", 'symmetrical': 'False'}),
            'common_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'common_destination': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destination'", 'to': "orm['stops.BaseStop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'origin'", 'to': "orm['stops.BaseStop']"})
        },
        'stops.source': {
            'Meta': {'object_name': 'Source'},
            'encoding': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'stops.sourceattribute': {
            'Meta': {'unique_together': "(('stop', 'key'),)", 'object_name': 'SourceAttribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Source']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.BaseStop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'stops.stopattribute': {
            'Meta': {'unique_together': "(('stop', 'key'),)", 'object_name': 'StopAttribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.BaseStop']"}),
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
            'from_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_stop'", 'to': "orm['stops.BaseStop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'to_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_stop'", 'to': "orm['stops.BaseStop']"}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Trip']"})
        },
        'stops.userstop': {
            'Meta': {'object_name': 'UserStop', '_ormbases': ['stops.BaseStop']},
            'basestop_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['stops.BaseStop']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parent'", 'null': 'True', 'to': "orm['stops.BaseStop']"}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'tpc': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        }
    }

    complete_apps = ['stops']
