# Generated by Django 3.0.5 on 2020-05-05 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_authgroup_authgrouppermissions_authpermission_authuser_authusergroups_authuseruserpermissions_django'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='musicdataget',
            options={},
        ),
        migrations.AlterModelOptions(
            name='musicdataintegrated',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='musicdatasend',
            options={'managed': True},
        ),
    ]
