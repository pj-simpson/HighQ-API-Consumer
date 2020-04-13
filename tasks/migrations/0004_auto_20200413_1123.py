# Generated by Django 3.0.3 on 2020-04-13 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20200411_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('in_progress', 'In Progress'), ('complete', 'Complete')], default='new', max_length=12),
        ),
    ]
