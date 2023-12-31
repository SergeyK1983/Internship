# Generated by Django 4.2.7 on 2023-12-24 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perevalinfo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perevaladded',
            old_name='beautyTitle',
            new_name='beauty_title',
        ),
        migrations.RemoveField(
            model_name='users',
            name='pereval_id',
        ),
        migrations.AddField(
            model_name='perevaladded',
            name='users_id',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='pereval', to='perevalinfo.users', verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='perevalimages',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='difficultylevel',
            name='autumn',
            field=models.CharField(blank=True, choices=[('LV1', '1А'), ('LV2', '1Б'), ('LV3', '2А'), ('LV4', '2Б'), ('LV5', '3А'), ('LV6', '3Б')], default='LV1', max_length=3, null=True, verbose_name='Осень'),
        ),
        migrations.AlterField(
            model_name='difficultylevel',
            name='spring',
            field=models.CharField(blank=True, choices=[('LV1', '1А'), ('LV2', '1Б'), ('LV3', '2А'), ('LV4', '2Б'), ('LV5', '3А'), ('LV6', '3Б')], default='LV1', max_length=3, null=True, verbose_name='Весна'),
        ),
        migrations.AlterField(
            model_name='difficultylevel',
            name='summer',
            field=models.CharField(blank=True, choices=[('LV1', '1А'), ('LV2', '1Б'), ('LV3', '2А'), ('LV4', '2Б'), ('LV5', '3А'), ('LV6', '3Б')], default='LV1', max_length=3, null=True, verbose_name='Лето'),
        ),
        migrations.AlterField(
            model_name='difficultylevel',
            name='winter',
            field=models.CharField(blank=True, choices=[('LV1', '1А'), ('LV2', '1Б'), ('LV3', '2А'), ('LV4', '2Б'), ('LV5', '3А'), ('LV6', '3Б')], default='LV1', max_length=3, null=True, verbose_name='Зима'),
        ),
        migrations.AlterField(
            model_name='perevaladded',
            name='coord_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coord', to='perevalinfo.coords', verbose_name='Координаты'),
        ),
        migrations.AlterField(
            model_name='perevaladded',
            name='status',
            field=models.CharField(choices=[('NW', 'Новый'), ('PN', 'В работе'), ('AC', 'Принято'), ('RJ', 'Не принято')], default='NW', max_length=2, verbose_name='Состояние'),
        ),
    ]
