# Generated by Django 3.0.5 on 2021-11-20 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_auto_20211120_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='questionimg',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
    ]
