# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WorldBorder'
        db.create_table('stops_worldborder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('area', self.gf('django.db.models.fields.IntegerField')()),
            ('pop2005', self.gf('django.db.models.fields.IntegerField')()),
            ('fips', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('iso2', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('iso3', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('un', self.gf('django.db.models.fields.IntegerField')()),
            ('region', self.gf('django.db.models.fields.IntegerField')()),
            ('subregion', self.gf('django.db.models.fields.IntegerField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('mpoly', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('stops', ['WorldBorder'])

        # Adding model 'Agency'
        db.create_table('stops_agency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_is_trash', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='is_trash')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('stops', ['Agency'])

        # Adding model 'Stop'
        db.create_table('stops_stop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_is_trash', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='is_trash')),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('common_city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('stops', ['Stop'])

        # Adding model 'StopAttribute'
        db.create_table('stops_stopattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_is_trash', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='is_trash')),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('stops', ['StopAttribute'])

        # Adding model 'AgencyAttribute'
        db.create_table('stops_agencyattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_is_trash', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='is_trash')),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Agency'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('stops', ['AgencyAttribute'])


    def backwards(self, orm):
        
        # Deleting model 'WorldBorder'
        db.delete_table('stops_worldborder')

        # Deleting model 'Agency'
        db.delete_table('stops_agency')

        # Deleting model 'Stop'
        db.delete_table('stops_stop')

        # Deleting model 'StopAttribute'
        db.delete_table('stops_stopattribute')

        # Deleting model 'AgencyAttribute'
        db.delete_table('stops_agencyattribute')


    models = {
        'stops.agency': {
            'Meta': {'object_name': 'Agency'},
            '_is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_trash'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'stops.agencyattribute': {
            'Meta': {'object_name': 'AgencyAttribute'},
            '_is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_trash'"}),
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Agency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Stop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'stops.stop': {
            'Meta': {'object_name': 'Stop'},
            '_is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_trash'"}),
            'common_city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        'stops.stopattribute': {
            'Meta': {'object_name': 'StopAttribute'},
            '_is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_trash'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Stop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'stops.worldborder': {
            'Meta': {'object_name': 'WorldBorder'},
            'area': ('django.db.models.fields.IntegerField', [], {}),
            'fips': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pop2005': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.IntegerField', [], {}),
            'subregion': ('django.db.models.fields.IntegerField', [], {}),
            'un': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['stops']
