# Generated by Django 3.1.2 on 2020-10-08 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0004_auto_20201008_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='livedoubtsession',
            name='subjects',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='edu.subject'),
        ),
    ]
