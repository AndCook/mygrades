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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('end_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('is_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_current', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_future', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hours_planned', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hours_passed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gpa_hours', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gpa_points', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('final_gpa', self.gf('django.db.models.fields.FloatField')(default=-1.0)),
            ('cumulative_gpa', self.gf('django.db.models.fields.FloatField')(default=-1.0)),
            ('cumulative_hours_passed', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'gradebook', ['Semester'])

        # Adding model 'Course'
        db.create_table(u'gradebook_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('hours', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('instructor', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gradebook.Semester'])),
            ('final_grade', self.gf('django.db.models.fields.CharField')(default='#', max_length=2)),
            ('gpa_points', self.gf('django.db.models.fields.FloatField')(default=0)),
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
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'final_grade': ('django.db.models.fields.CharField', [], {'default': "'#'", 'max_length': '2'}),
            'gpa_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gradebook.Semester']"})
        },
        u'gradebook.semester': {
            'Meta': {'object_name': 'Semester'},
            'cumulative_gpa': ('django.db.models.fields.FloatField', [], {'default': '-1.0'}),
            'cumulative_hours_passed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'final_gpa': ('django.db.models.fields.FloatField', [], {'default': '-1.0'}),
            'gpa_hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gpa_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'hours_passed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hours_planned': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_future': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['gradebook']