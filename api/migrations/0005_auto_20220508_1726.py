# Generated by Django 3.1.2 on 2022-05-08 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20220508_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('ongoing', 'ongoing'), ('finished', 'finished')], max_length=200),
        ),
    ]