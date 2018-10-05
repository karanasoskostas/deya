# Generated by Django 2.0.7 on 2018-10-04 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('damage', '0028_contactdetails_userip'),
    ]

    operations = [
        migrations.CreateModel(
            name='DamageHistoryStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField()),
                ('com', models.CharField(default=None, max_length=500, null=True)),
                ('userip', models.CharField(default=None, max_length=100, null=True)),
                ('damage', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='damage.Damage')),
                ('damagestatus', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='damage.DamageStatus')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
