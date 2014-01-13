# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Semester'
        db.create_table(u'gradebook_semester', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'gradebook', ['Semester'])

        # Adding model 'Course'
        db.create_table(u'gradebook_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('instructor', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradebook.Semester'])),
        ))
        db.send_create_signal(u'gradebook', ['Course'])

        # Adding model 'Category'
        db.create_table(u'gradebook_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('worth', self.gf('django.db.models.fields.FloatField')()),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradebook.Course'])),
        ))
        db.send_create_signal(u'gradebook', ['Category'])

        # Adding model 'Assignment'
        db.create_table(u'gradebook_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('awardedPoints', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('possiblePoints', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('percentage', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradebook.Category'])),
        ))
        db.send_create_signal(u'gradebook', ['Assignment'])


    def backwards(self, orm):
        # Deleting model 'Semester'
        db.delete_table(u'gradebook_semester')

        # Deleting model 'Course'
        db.delete_table(u'gradebook_course')

        # Deleting model 'Category'
        db.delete_table(u'gradebook_category')

        # Deleting model 'Assignment'
        db.delete_table(u'gradebook_assignment')


    models = {
        u'gradebook.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'awardedPoints': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gradebook.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'possiblePoints': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'gradebook.category': {
            'Meta': {'object_name': 'Category'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gradebook.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'worth': ('django.db.models.fields.FloatField', [], {})
        },
        u'gradebook.course': {
            'Meta': {'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gradebook.Semester']"})
        },
        u'gradebook.semester': {
            'Meta': {'object_name': 'Semester'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['gradebook']