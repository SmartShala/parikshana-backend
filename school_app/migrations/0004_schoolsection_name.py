# Generated by Django 4.0.6 on 2022-08-20 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0003_schoolsection_delete_schoolclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolsection',
            name='name',
            field=models.CharField(default='A', max_length=1),
        ),
    ]
