# Generated by Django 4.0.6 on 2022-08-25 19:29

from django.db import migrations, models
import django.db.models.deletion
import django_minio_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0012_test_is_shuffled'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='test_question_pdf',
            field=models.FileField(blank=True, null=True, storage=django_minio_backend.models.MinioBackend(bucket_name='parikshana-media'), upload_to='test_papers', verbose_name='test papers'),
        ),
        migrations.AlterField(
            model_name='test',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_topic', to='test_app.topic'),
        ),
    ]
