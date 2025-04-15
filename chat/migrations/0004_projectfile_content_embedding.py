from django.db import migrations, models
from pgvector.django import VectorField


class Migration(migrations.Migration):
    dependencies = [
        ('chat', '0003_enable_vector'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectfile',
            name='content',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectfile',
            name='embedding',
            field=VectorField(dimensions=768, null=True),
        ),
    ]    