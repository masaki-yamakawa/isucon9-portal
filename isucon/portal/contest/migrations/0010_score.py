# Generated by Django 2.2.1 on 2019-08-16 04:58

from django.db import migrations, models
import django.db.models.deletion
import isucon.portal.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_remove_team_aggregated_score'),
        ('contest', '0009_delete_aggregatedscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_score', models.IntegerField(default=0, verbose_name='ベストスコア')),
                ('latest_score', models.IntegerField(default=0, verbose_name='最新スコア')),
                ('total_score', models.IntegerField(default=0, verbose_name='累計スコア')),
                ('latest_is_passed', models.BooleanField(blank=True, default=False, verbose_name='最新のベンチマーク成否フラグ')),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.Team')),
            ],
            options={
                'verbose_name': 'チームスコア',
                'verbose_name_plural': 'チームスコア',
                'ordering': ('-latest_score', 'team'),
            },
            bases=(isucon.portal.models.LogicalDeleteMixin, models.Model),
        ),
    ]
