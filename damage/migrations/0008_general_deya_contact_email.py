# Generated by Django 2.1.2 on 2018-10-09 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('damage', '0007_remove_general_deya_contact_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='general',
            name='deya_contact_email',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
