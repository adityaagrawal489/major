# Generated by Django 3.0.5 on 2021-11-21 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_auto_20211121_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='totaltime',
            field=models.IntegerField(blank=True, default=100, help_text='duration of the quiz in minutes', null=True),
        ),
    ]
