# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Stop.stop_type'
        db.add_column('stops_stop', 'stop_type', self.gf('django.db.models.fields.SmallIntegerField')(default=1), keep_default=False)

        # Adding field 'Stop.parent'
        db.add_column('stops_stop', 'parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Stop.stop_type'
        db.delete_column('stops_stop', 'stop_type')

        # Deleting field 'Stop.parent'
        db.delete_column('stops_stop', 'parent_id')


    models = {
        'stops.agency': {
            'Meta': {'object_name': 'Agency'},
            'agency_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tz': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stops.agencyattribute': {
            'Meta': {'unique_together': "(('stop', 'key'),)", 'object_name': 'AgencyAttribute'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Agency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
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
            'tpc': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'stops.stopattribute': {
            'Meta': {'unique_together': "(('stop', 'key'),)", 'object_name': 'StopAttribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Stop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['stops']
