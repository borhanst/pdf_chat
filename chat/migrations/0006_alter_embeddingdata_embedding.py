# Generated by Django 5.2 on 2025-04-11 12:50

import pgvector.django.vector
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_remove_projectfile_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embeddingdata',
            name='embedding',
            field=pgvector.django.vector.VectorField(dimensions=768, null=True),
        ),
    ]
