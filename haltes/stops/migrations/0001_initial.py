# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Agency'
        db.create_table('stops_agency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tz', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('stops', ['Agency'])

        # Adding model 'Stop'
        db.create_table('stops_stop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('common_city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tpc', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('stops', ['Stop'])

        # Adding model 'StopAttribute'
        db.create_table('stops_stopattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('stops', ['StopAttribute'])

        # Adding unique constraint on 'StopAttribute', fields ['stop', 'key']
        db.create_unique('stops_stopattribute', ['stop_id', 'key'])

        # Adding model 'AgencyAttribute'
        db.create_table('stops_agencyattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Agency'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('stops', ['AgencyAttribute'])

        # Adding unique constraint on 'AgencyAttribute', fields ['stop', 'key']
        db.create_unique('stops_agencyattribute', ['stop_id', 'key'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'AgencyAttribute', fields ['stop', 'key']
        db.delete_unique('stops_agencyattribute', ['stop_id', 'key'])

        # Removing unique constraint on 'StopAttribute', fields ['stop', 'key']
        db.delete_unique('stops_stopattribute', ['stop_id', 'key'])

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
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
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
