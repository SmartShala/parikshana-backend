# Generated by Django 4.0.6 on 2022-08-15 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader_app', '0004_answersheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentgrade',
            name='ansQs',
            field=models.ManyToManyField(to='grader_app.answeredquestion'),
        ),
    ]