# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Source.encoding'
        db.alter_column(u'stops_source', 'encoding', self.gf('django.db.models.fields.CharField')(max_length=15))

    def backwards(self, orm):

        # Changing field 'Source.encoding'
        db.alter_column(u'stops_source', 'encoding', self.gf('django.db.models.fields.CharField')(max_length=10))

    models = {
        u'stops.agency': {
            'Meta': {'object_name': 'Agency'},
            'agency_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tz': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'stops.basestop': {
            'Meta': {'object_name': 'BaseStop'},
            'common_city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stop_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'stops.route': {
            'Meta': {'object_name': 'Route'},
            'agencies': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stops.Agency']", 'symmetrical': 'False'}),
            'common_code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'common_destination': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destination'", 'to': u"orm['stops.BaseStop']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'origin'", 'to': u"orm['stops.BaseStop']"})
        },
        u'stops.source': {
            'Meta': {'object_name': 'Source'},
            'encoding': ('django.db.models.fields.CharField', [], {'default': "'utf-8'", 'max_length': '15', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'stops.sourceattribute': {
            'Meta': {'unique_together': "(('stop', 'key'),)", 'object_name': 'SourceAttribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Source']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.BaseStop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'stops.stopattribute': {
            'Meta': {'unique_together': "(('stop', 'key'),)", 'object_name': 'StopAttribute'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.BaseStop']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'stops.trip': {
            'Meta': {'object_name': 'Trip'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Route']"}),
            'trip_id': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'stops.tripsegment': {
            'Meta': {'object_name': 'TripSegment'},
            'from_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_stop'", 'to': u"orm['stops.BaseStop']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'to_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_stop'", 'to': u"orm['stops.BaseStop']"}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Trip']"})
        },
        u'stops.userstop': {
            'Meta': {'object_name': 'UserStop', '_ormbases': [u'stops.BaseStop']},
            u'basestop_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['stops.BaseStop']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parent'", 'null': 'True', 'to': u"orm['stops.BaseStop']"}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'tpc': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        }
    }

    complete_apps = ['stops']