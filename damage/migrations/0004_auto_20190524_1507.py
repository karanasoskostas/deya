# Generated by Django 2.1.2 on 2019-05-24 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('damage', '0003_auto_20181105_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='general',
            name='deya_latitude',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=13, null=True),
        ),
        migrations.AlterField(
            model_name='general',
            name='deya_longitude',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=13, null=True),
        ),
    ]
