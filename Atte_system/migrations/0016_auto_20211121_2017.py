# Generated by Django 3.0.5 on 2021-11-21 14:47

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Atte_system', '0015_auto_20211121_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question',
            field=django_quill.fields.QuillField(),
        ),
    ]