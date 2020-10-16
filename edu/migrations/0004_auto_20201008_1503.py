# Generated by Django 3.1.2 on 2020-10-08 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0003_auto_20201005_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livedoubtsession',
            name='day_and_time',
        ),
        migrations.AddField(
            model_name='livedoubtsession',
            name='day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='livedoubtsession',
            name='from_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='livedoubtsession',
            name='to_time',
            field=models.TimeField(null=True),
        ),
    ]
