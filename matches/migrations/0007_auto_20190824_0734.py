# Generated by Django 2.2.4 on 2019-08-23 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0006_auto_20190823_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='wtamatch',
            name='court',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='wtamatch',
            name='surface',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
