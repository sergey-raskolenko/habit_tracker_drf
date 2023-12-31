# Generated by Django 4.2.4 on 2023-11-13 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='periodicity',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Раз в 1 день'), (2, 'Раз в 2 дня'), (3, 'Раз в 3 дня'), (4, 'Раз в 4 дня'), (5, 'Раз в 5 дней'), (6, 'Раз в 6 дней'), (7, 'Раз в 7 дней')], verbose_name='Периодичность'),
        ),
    ]
