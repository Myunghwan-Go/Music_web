# Generated by Django 3.0.5 on 2020-05-07 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20200505_2107'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='commenttable',
            table='Comment_table',
        ),
        migrations.AlterModelTable(
            name='musicdataget',
            table='Music_data_get',
        ),
        migrations.AlterModelTable(
            name='musicdataintegrated',
            table='Music_data_integrated',
        ),
        migrations.AlterModelTable(
            name='musicdatasend',
            table='Music_data_send',
        ),
        migrations.AlterModelTable(
            name='postfiletable',
            table='Post_file_table',
        ),
        migrations.AlterModelTable(
            name='recommendtable',
            table='Recommend_table',
        ),
        migrations.AlterModelTable(
            name='sharetable',
            table='Share_table',
        ),
        migrations.AlterModelTable(
            name='user',
            table='User',
        ),
    ]
