# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'StopAttribute', fields ['stop', 'key']
        db.create_unique('stops_stopattribute', ['stop_id', 'key'])

        # Adding unique constraint on 'AgencyAttribute', fields ['stop', 'key']
        db.create_unique('stops_agencyattribute', ['stop_id', 'key'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'AgencyAttribute', fields ['stop', 'key']
        db.delete_unique('stops_agencyattribute', ['stop_id', 'key'])

        # Removing unique constraint on 'StopAttribute', fields ['stop', 'key']
        db.delete_unique('stops_stopattribute', ['stop_id', 'key'])


    models = {
        'stops.agency': {
            'Meta': {'object_name': 'Agency'},
            '_is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_trash'"}),
            'agency_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tz': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'stops.agencyattribute': {
            'Meta': {'unique_together': "(('stop', 'key'),)", 'object_name': 'AgencyAttribute'},
            '_is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_trash'"}),
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Agency']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Stop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'stops.stop': {
            'Meta': {'object_name': 'Stop'},
            '_is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_trash'"}),
            'common_city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'tpc': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'stops.stopattribute': {
            'Meta': {'unique_together': "(('stop', 'key'),)", 'object_name': 'StopAttribute'},
            '_is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_trash'"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Stop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['stops']
