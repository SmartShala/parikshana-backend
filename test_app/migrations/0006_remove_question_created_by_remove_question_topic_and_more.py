# Generated by Django 4.0.6 on 2022-08-20 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0005_alter_topic_board'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='question',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='question',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='test',
            name='questions',
        ),
        migrations.AddField(
            model_name='question',
            name='marks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_mapping', to='test_app.test'),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_option',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='options',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.DeleteModel(
            name='TestQuestionMapping',
        ),
    ]
