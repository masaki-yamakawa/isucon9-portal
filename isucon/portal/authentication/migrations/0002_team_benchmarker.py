# Generated by Django 2.2.1 on 2019-05-31 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_remove_server_benchmarker'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='benchmarker',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='resources.Benchmarker', verbose_name='ベンチマーカー'),
            preserve_default=False,
        ),
    ]
