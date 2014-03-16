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

        # Adding model 'Source'
        db.create_table('stops_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_id', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('stops', ['Source'])

        # Adding model 'BaseStop'
        db.create_table('stops_basestop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('common_city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('stop_type', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('stops', ['BaseStop'])

        # Adding model 'UserStop'
        db.create_table('stops_userstop', (
            ('basestop_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['stops.BaseStop'], unique=True, primary_key=True)),
            ('tpc', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='parent', null=True, to=orm['stops.BaseStop'])),
        ))
        db.send_create_signal('stops', ['UserStop'])

        # Adding model 'StopAttribute'
        db.create_table('stops_stopattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.BaseStop'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('stops', ['StopAttribute'])

        # Adding unique constraint on 'StopAttribute', fields ['stop', 'key']
        db.create_unique('stops_stopattribute', ['stop_id', 'key'])

        # Adding model 'SourceAttribute'
        db.create_table('stops_sourceattribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.BaseStop'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Source'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('stops', ['SourceAttribute'])

        # Adding unique constraint on 'SourceAttribute', fields ['stop', 'key']
        db.create_unique('stops_sourceattribute', ['stop_id', 'key'])

        # Adding model 'Route'
        db.create_table('stops_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('common_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('common_destination', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('origin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='origin', to=orm['stops.BaseStop'])),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='destination', to=orm['stops.BaseStop'])),
        ))
        db.send_create_signal('stops', ['Route'])

        # Adding M2M table for field agencies on 'Route'
        db.create_table('stops_route_agencies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('route', models.ForeignKey(orm['stops.route'], null=False)),
            ('agency', models.ForeignKey(orm['stops.agency'], null=False))
        ))
        db.create_unique('stops_route_agencies', ['route_id', 'agency_id'])

        # Adding model 'Trip'
        db.create_table('stops_trip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Route'])),
        ))
        db.send_create_signal('stops', ['Trip'])

        # Adding model 'TripSegment'
        db.create_table('stops_tripsegment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Trip'])),
            ('from_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_stop', to=orm['stops.BaseStop'])),
            ('to_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_stop', to=orm['stops.BaseStop'])),
            ('line', self.gf('django.contrib.gis.db.models.fields.LineStringField')()),
        ))
        db.send_create_signal('stops', ['TripSegment'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'SourceAttribute', fields ['stop', 'key']
        db.delete_unique('stops_sourceattribute', ['stop_id', 'key'])

        # Removing unique constraint on 'StopAttribute', fields ['stop', 'key']
        db.delete_unique('stops_stopattribute', ['stop_id', 'key'])

        # Deleting model 'Agency'
        db.delete_table('stops_agency')

        # Deleting model 'Source'
        db.delete_table('stops_source')

        # Deleting model 'BaseStop'
        db.delete_table('stops_basestop')

        # Deleting model 'UserStop'
        db.delete_table('stops_userstop')

        # Deleting model 'StopAttribute'
        db.delete_table('stops_stopattribute')

        # Deleting model 'SourceAttribute'
        db.delete_table('stops_sourceattribute')

        # Deleting model 'Route'
        db.delete_table('stops_route')

        # Removing M2M table for field agencies on 'Route'
        db.delete_table('stops_route_agencies')

        # Deleting model 'Trip'
        db.delete_table('stops_trip')

        # Deleting model 'TripSegment'
        db.delete_table('stops_tripsegment')


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
