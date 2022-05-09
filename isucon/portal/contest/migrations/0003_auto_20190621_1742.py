# Generated by Django 2.2.2 on 2019-06-21 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20190603_1824'),
        ('contest', '0002_auto_20190610_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregatedScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_score', models.IntegerField(default=0, verbose_name='ベストスコア')),
                ('latest_score', models.IntegerField(default=0, verbose_name='最新獲得スコア')),
                ('latest_is_passed', models.BooleanField(blank=True, default=False, verbose_name='最新のベンチマーク成否フラグ')),
            ],
            options={
                'verbose_name': '集計スコア',
                'verbose_name_plural': '集計スコア',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('waiting', 'waiting'), ('running', 'running'), ('done', 'done'), ('aborted', 'aborted'), ('canceled', 'canceled')], default='waiting', max_length=100, verbose_name='進捗')),
                ('is_passed', models.BooleanField(default=False, verbose_name='正答フラグ')),
                ('score', models.IntegerField(default=0, verbose_name='獲得スコア')),
                ('total_score', models.IntegerField(verbose_name='累計スコア')),       
                ('result_json', models.TextField(verbose_name='結果JSON')),
                ('log_text', models.TextField(verbose_name='ログ文字列')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='最終更新日時')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.Team', verbose_name='チーム')),
            ],
            options={
                'verbose_name': 'ジョブ',
                'verbose_name_plural': 'ジョブ',
                'ordering': ('-created_at',),
            },
        ),
        migrations.RemoveField(
            model_name='benchmarker',
            name='network',
        ),
        migrations.RemoveField(
            model_name='benchmarker',
            name='node',
        ),
        migrations.RemoveField(
            model_name='server',
            name='private_network',
        ),
        migrations.AddField(
            model_name='server',
            name='is_bench_target',
            field=models.BooleanField(default=False, verbose_name='ベンチマークターゲットであるかのフラグ'),
        ),
        migrations.AlterField(
            model_name='benchmarker',
            name='ip',
            field=models.CharField(max_length=100, verbose_name='ベンチマーカーのIPアドレス'),
        ),
        migrations.AlterField(
            model_name='scorehistory',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='contest.Job', verbose_name='ベンチキュー'),
        ),
        migrations.DeleteModel(
            name='BenchQueue',
        ),
    ]
