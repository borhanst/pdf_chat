# Generated by Django 5.2 on 2025-04-11 12:34

import django.db.models.deletion
import pgvector.django.vector
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_projectfile_content_embedding'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectfile',
            name='content',
        ),
        migrations.RemoveField(
            model_name='projectfile',
            name='embedding',
        ),
        migrations.CreateModel(
            name='EmbeddingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('content', models.TextField(null=True)),
                ('embedding', pgvector.django.vector.VectorField(dimensions=1536, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
