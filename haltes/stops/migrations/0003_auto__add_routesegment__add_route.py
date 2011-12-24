# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RouteSegment'
        db.create_table('stops_routesegment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Route'])),
            ('from_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_stop', to=orm['stops.Stop'])),
            ('to_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_stop', to=orm['stops.Stop'])),
            ('line', self.gf('django.contrib.gis.db.models.fields.LineStringField')()),
        ))
        db.send_create_signal('stops', ['RouteSegment'])

        # Adding model 'Route'
        db.create_table('stops_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('common_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('common_destination', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('origin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='origin', to=orm['stops.Stop'])),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='destination', to=orm['stops.Stop'])),
        ))
        db.send_create_signal('stops', ['Route'])

        # Adding M2M table for field agencies on 'Route'
        db.create_table('stops_route_agencies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('route', models.ForeignKey(orm['stops.route'], null=False)),
            ('agency', models.ForeignKey(orm['stops.agency'], null=False))
        ))
        db.create_unique('stops_route_agencies', ['route_id', 'agency_id'])


    def backwards(self, orm):
        
        # Deleting model 'RouteSegment'
        db.delete_table('stops_routesegment')

        # Deleting model 'Route'
        db.delete_table('stops_route')

        # Removing M2M table for field agencies on 'Route'
        db.delete_table('stops_route_agencies')


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
        'stops.route': {
            'Meta': {'object_name': 'Route'},
            'agencies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['stops.Agency']", 'symmetrical': 'False'}),
            'common_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'common_destination': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destination'", 'to': "orm['stops.Stop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'origin'", 'to': "orm['stops.Stop']"})
        },
        'stops.routesegment': {
            'Meta': {'object_name': 'RouteSegment'},
            'from_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_stop'", 'to': "orm['stops.Stop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stops.Route']"}),
            'to_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_stop'", 'to': "orm['stops.Stop']"})
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
