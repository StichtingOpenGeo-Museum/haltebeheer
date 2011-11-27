# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Agency'
        db.create_table('stops_agency', (
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('_is_trash', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='is_trash')),
            ('agency_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tz', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('stops', ['Agency'])

        # Adding model 'Stop'
        db.create_table('stops_stop', (
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('_is_trash', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='is_trash')),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('common_city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('stops', ['Stop'])

        # Adding model 'StopAttribute'
        db.create_table('stops_stopattribute', (
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('_is_trash', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='is_trash')),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('stops', ['StopAttribute'])

        # Adding model 'AgencyAttribute'
        db.create_table('stops_agencyattribute', (
            ('vid', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, db_index=True)),
            ('_is_trash', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='is_trash')),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Agency'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('stops', ['AgencyAttribute'])


    def backwards(self, orm):
        
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
            'agency_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tz': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'stops.agencyattribute': {
            'Meta': {'object_name': 'AgencyAttribute'},
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
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'stops.stopattribute': {
            'Meta': {'object_name': 'StopAttribute'},
            '_is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'is_trash'"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'db_index': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Stop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'vid': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['stops']
