# Generated by Django 2.2.3 on 2019-07-31 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0002_atpmatch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atpmatch',
            name='iswinhome',
        ),
        migrations.AddField(
            model_name='atpmatch',
            name='away',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='atpmatch',
            name='home',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
