# Generated by Django 4.0.1 on 2022-01-20 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dpa_app', '0002_alter_group_options_alter_pm_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pm',
            options={'verbose_name': 'ПМа', 'verbose_name_plural': 'ПМы'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Ученика', 'verbose_name_plural': 'Ученики'},
        ),
    ]