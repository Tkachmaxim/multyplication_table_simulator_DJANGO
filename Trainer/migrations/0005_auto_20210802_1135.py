# Generated by Django 3.2.4 on 2021-08-02 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trainer', '0004_alter_game_number_example'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='a',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='b',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='game',
            name='result',
            field=models.CharField(max_length=20),
        ),
    ]