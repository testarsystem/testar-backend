# Generated by Django 2.2.7 on 2019-11-06 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testn', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
