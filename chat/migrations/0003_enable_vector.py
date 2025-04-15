from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('chat', '0002_remove_project_file_project_slug_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            'CREATE EXTENSION IF NOT EXISTS vector;',
            'DROP EXTENSION IF EXISTS vector;'
        ),
    ]    