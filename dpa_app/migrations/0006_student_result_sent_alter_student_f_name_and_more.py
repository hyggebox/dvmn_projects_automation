# Generated by Django 4.0.1 on 2022-01-23 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dpa_app', '0005_senddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='result_sent',
            field=models.BooleanField(default=False, verbose_name='Результаты распределения отправлены'),
        ),
        migrations.AlterField(
            model_name='student',
            name='f_name',
            field=models.CharField(max_length=200, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='student',
            name='l_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='student',
            name='level',
            field=models.CharField(max_length=200, verbose_name='Уровень'),
        ),
        migrations.AlterField(
            model_name='student',
            name='link_sent',
            field=models.BooleanField(default=False, verbose_name='Ссылка на форму отправлена'),
        ),
        migrations.AlterField(
            model_name='student',
            name='tg_id',
            field=models.IntegerField(verbose_name='ID в Telegram'),
        ),
    ]
