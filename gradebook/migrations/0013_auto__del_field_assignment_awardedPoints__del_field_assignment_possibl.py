# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Assignment.awardedPoints'
        db.delete_column(u'gradebook_assignment', 'awardedPoints')

        # Deleting field 'Assignment.possiblePoints'
        db.delete_column(u'gradebook_assignment', 'possiblePoints')

        # Adding field 'Assignment.grade_unknown'
        db.add_column(u'gradebook_assignment', 'grade_unknown',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Assignment.points_earned'
        db.add_column(u'gradebook_assignment', 'points_earned',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Assignment.total_points'
        db.add_column(u'gradebook_assignment', 'total_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


        # Changing field 'Assignment.percentage'
        db.alter_column(u'gradebook_assignment', 'percentage', self.gf('django.db.models.fields.FloatField')())
        # Deleting field 'Semester.grade_points'
        db.delete_column(u'gradebook_semester', 'grade_points')

        # Adding field 'Semester.final_grade_points'
        db.add_column(u'gradebook_semester', 'final_grade_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Semester.cumulative_gpa_hours'
        db.add_column(u'gradebook_semester', 'cumulative_gpa_hours',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Semester.potential_min_grade_points'
        db.add_column(u'gradebook_semester', 'potential_min_grade_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Semester.potential_grade_points'
        db.add_column(u'gradebook_semester', 'potential_grade_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Semester.potential_max_grade_points'
        db.add_column(u'gradebook_semester', 'potential_max_grade_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Semester.potential_hours_counted'
        db.add_column(u'gradebook_semester', 'potential_hours_counted',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Semester.potential_min_gpa'
        db.add_column(u'gradebook_semester', 'potential_min_gpa',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Semester.potential_gpa'
        db.add_column(u'gradebook_semester', 'potential_gpa',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Semester.potential_max_gpa'
        db.add_column(u'gradebook_semester', 'potential_max_gpa',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Deleting field 'Course.grade_points'
        db.delete_column(u'gradebook_course', 'grade_points')

        # Adding field 'Course.final_grade_points'
        db.add_column(u'gradebook_course', 'final_grade_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Course.not_specified_worth'
        db.add_column(u'gradebook_course', 'not_specified_worth',
                      self.gf('django.db.models.fields.FloatField')(default=100),
                      keep_default=False)

        # Adding field 'Course.total_weighted_percentage'
        db.add_column(u'gradebook_course', 'total_weighted_percentage',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Course.total_worth_used'
        db.add_column(u'gradebook_course', 'total_worth_used',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Course.course_grade'
        db.add_column(u'gradebook_course', 'course_grade',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Course.min_weighted_percentage'
        db.add_column(u'gradebook_course', 'min_weighted_percentage',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Course.course_min_grade'
        db.add_column(u'gradebook_course', 'course_min_grade',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Course.max_weighted_percentage'
        db.add_column(u'gradebook_course', 'max_weighted_percentage',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Course.course_max_grade'
        db.add_column(u'gradebook_course', 'course_max_grade',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Course.course_grade_points'
        db.add_column(u'gradebook_course', 'course_grade_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Course.course_min_grade_points'
        db.add_column(u'gradebook_course', 'course_min_grade_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Course.course_max_grade_points'
        db.add_column(u'gradebook_course', 'course_max_grade_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Category.actual_points_earned'
        db.add_column(u'gradebook_category', 'actual_points_earned',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Category.actual_total_points'
        db.add_column(u'gradebook_category', 'actual_total_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Category.max_points_earned'
        db.add_column(u'gradebook_category', 'max_points_earned',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Category.total_points'
        db.add_column(u'gradebook_category', 'total_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Category.category_percentage'
        db.add_column(u'gradebook_category', 'category_percentage',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Category.category_weighted_percentage'
        db.add_column(u'gradebook_category', 'category_weighted_percentage',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Category.min_category_percentage'
        db.add_column(u'gradebook_category', 'min_category_percentage',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Category.max_category_percentage'
        db.add_column(u'gradebook_category', 'max_category_percentage',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Category.min_category_weighted_percentage'
        db.add_column(u'gradebook_category', 'min_category_weighted_percentage',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'Category.max_category_weighted_percentage'
        db.add_column(u'gradebook_category', 'max_category_weighted_percentage',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Assignment.awardedPoints'
        db.add_column(u'gradebook_assignment', 'awardedPoints',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2),
                      keep_default=False)

        # Adding field 'Assignment.possiblePoints'
        db.add_column(u'gradebook_assignment', 'possiblePoints',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=2),
                      keep_default=False)

        # Deleting field 'Assignment.grade_unknown'
        db.delete_column(u'gradebook_assignment', 'grade_unknown')

        # Deleting field 'Assignment.points_earned'
        db.delete_column(u'gradebook_assignment', 'points_earned')

        # Deleting field 'Assignment.total_points'
        db.delete_column(u'gradebook_assignment', 'total_points')


        # Changing field 'Assignment.percentage'
        db.alter_column(u'gradebook_assignment', 'percentage', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2))
        # Adding field 'Semester.grade_points'
        db.add_column(u'gradebook_semester', 'grade_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Deleting field 'Semester.final_grade_points'
        db.delete_column(u'gradebook_semester', 'final_grade_points')

        # Deleting field 'Semester.cumulative_gpa_hours'
        db.delete_column(u'gradebook_semester', 'cumulative_gpa_hours')

        # Deleting field 'Semester.potential_min_grade_points'
        db.delete_column(u'gradebook_semester', 'potential_min_grade_points')

        # Deleting field 'Semester.potential_grade_points'
        db.delete_column(u'gradebook_semester', 'potential_grade_points')

        # Deleting field 'Semester.potential_max_grade_points'
        db.delete_column(u'gradebook_semester', 'potential_max_grade_points')

        # Deleting field 'Semester.potential_hours_counted'
        db.delete_column(u'gradebook_semester', 'potential_hours_counted')

        # Deleting field 'Semester.potential_min_gpa'
        db.delete_column(u'gradebook_semester', 'potential_min_gpa')

        # Deleting field 'Semester.potential_gpa'
        db.delete_column(u'gradebook_semester', 'potential_gpa')

        # Deleting field 'Semester.potential_max_gpa'
        db.delete_column(u'gradebook_semester', 'potential_max_gpa')

        # Adding field 'Course.grade_points'
        db.add_column(u'gradebook_course', 'grade_points',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Deleting field 'Course.final_grade_points'
        db.delete_column(u'gradebook_course', 'final_grade_points')

        # Deleting field 'Course.not_specified_worth'
        db.delete_column(u'gradebook_course', 'not_specified_worth')

        # Deleting field 'Course.total_weighted_percentage'
        db.delete_column(u'gradebook_course', 'total_weighted_percentage')

        # Deleting field 'Course.total_worth_used'
        db.delete_column(u'gradebook_course', 'total_worth_used')

        # Deleting field 'Course.course_grade'
        db.delete_column(u'gradebook_course', 'course_grade')

        # Deleting field 'Course.min_weighted_percentage'
        db.delete_column(u'gradebook_course', 'min_weighted_percentage')

        # Deleting field 'Course.course_min_grade'
        db.delete_column(u'gradebook_course', 'course_min_grade')

        # Deleting field 'Course.max_weighted_percentage'
        db.delete_column(u'gradebook_course', 'max_weighted_percentage')

        # Deleting field 'Course.course_max_grade'
        db.delete_column(u'gradebook_course', 'course_max_grade')

        # Deleting field 'Course.course_grade_points'
        db.delete_column(u'gradebook_course', 'course_grade_points')

        # Deleting field 'Course.course_min_grade_points'
        db.delete_column(u'gradebook_course', 'course_min_grade_points')

        # Deleting field 'Course.course_max_grade_points'
        db.delete_column(u'gradebook_course', 'course_max_grade_points')

        # Deleting field 'Category.actual_points_earned'
        db.delete_column(u'gradebook_category', 'actual_points_earned')

        # Deleting field 'Category.actual_total_points'
        db.delete_column(u'gradebook_category', 'actual_total_points')

        # Deleting field 'Category.max_points_earned'
        db.delete_column(u'gradebook_category', 'max_points_earned')

        # Deleting field 'Category.total_points'
        db.delete_column(u'gradebook_category', 'total_points')

        # Deleting field 'Category.category_percentage'
        db.delete_column(u'gradebook_category', 'category_percentage')

        # Deleting field 'Category.category_weighted_percentage'
        db.delete_column(u'gradebook_category', 'category_weighted_percentage')

        # Deleting field 'Category.min_category_percentage'
        db.delete_column(u'gradebook_category', 'min_category_percentage')

        # Deleting field 'Category.max_category_percentage'
        db.delete_column(u'gradebook_category', 'max_category_percentage')

        # Deleting field 'Category.min_category_weighted_percentage'
        db.delete_column(u'gradebook_category', 'min_category_weighted_percentage')

        # Deleting field 'Category.max_category_weighted_percentage'
        db.delete_column(u'gradebook_category', 'max_category_weighted_percentage')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gradebook.Category']"}),
            'grade_unknown': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'points_earned': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'total_points': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'gradebook.category': {
            'Meta': {'object_name': 'Category'},
            'actual_points_earned': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'actual_total_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'category_percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'category_weighted_percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gradebook.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_category_percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'max_category_weighted_percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'max_points_earned': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'min_category_percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'min_category_weighted_percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'worth': ('django.db.models.fields.FloatField', [], {})
        },
        u'gradebook.course': {
            'Meta': {'object_name': 'Course'},
            'course_grade': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'course_grade_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'course_max_grade': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'course_max_grade_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'course_min_grade': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'course_min_grade_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'final_grade': ('django.db.models.fields.CharField', [], {'default': "'#'", 'max_length': '2'}),
            'final_grade_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'max_weighted_percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'min_weighted_percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'not_specified_worth': ('django.db.models.fields.FloatField', [], {'default': '100'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gradebook.Semester']"}),
            'total_weighted_percentage': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'total_worth_used': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'gradebook.semester': {
            'Meta': {'object_name': 'Semester'},
            'cumulative_gpa': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'cumulative_gpa_hours': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'cumulative_hours_passed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'final_gpa': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'final_grade_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'gpa_hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hours_passed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hours_planned': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_future': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'potential_gpa': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'potential_grade_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'potential_hours_counted': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'potential_max_gpa': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'potential_max_grade_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'potential_min_gpa': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'potential_min_grade_points': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['gradebook']