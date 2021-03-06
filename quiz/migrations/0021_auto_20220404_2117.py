# Generated by Django 3.0.5 on 2022-04-04 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0020_auto_20220403_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='Course',
            field=models.ManyToManyField(blank=True, null=True, related_name='Anshuman', to='quiz.Course'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='Course_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Course'),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('date', models.DateField()),
                ('Course_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Attendence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parens_or_not', models.BooleanField(default=False)),
                ('meeting_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Meeting')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quiz.Student')),
            ],
        ),
    ]
