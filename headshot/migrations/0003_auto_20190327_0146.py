# Generated by Django 2.0.5 on 2019-03-27 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('headshot', '0002_auto_20190326_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headshot',
            name='email',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='headshot',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Requested', 'Requested'), ('Reviewing', 'Reviewing'), ('In Progress', 'In Progress'), ('Accepted', 'Accepted'), ('Declined', 'Declined'), ('Canceled', 'Canceled'), ('Completed', 'Completed')], default='Draft', max_length=20),
        ),
    ]
