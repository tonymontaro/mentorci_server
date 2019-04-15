# Generated by Django 2.0.3 on 2019-04-14 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(default='', max_length=500)),
                ('concern', models.TextField(default='', max_length=500)),
                ('date', models.CharField(max_length=255)),
                ('types', models.CharField(max_length=255)),
                ('duration', models.CharField(max_length=255)),
                ('duration_in_mins', models.IntegerField()),
                ('feeling', models.TextField()),
                ('mentor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.Student')),
            ],
        ),
    ]
