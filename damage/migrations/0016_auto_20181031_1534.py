# Generated by Django 2.1.2 on 2018-10-31 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('damage', '0015_auto_20181031_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areas',
            name='code',
            field=models.IntegerField(unique=True),
        ),
    ]
