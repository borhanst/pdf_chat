from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from pgvector.django import VectorField


from config.mixins.models import BaseModelMixin


def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB limit
        raise ValidationError("The maximum file size that can be uploaded is 10MB")

    # Check file type
    file_extension = value.name.split(".")[-1].lower()
    if file_extension != "pdf":
        raise ValidationError("Only PDF files are allowed")


class Project(BaseModelMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def file_count(self):
        return self.projectfile_set.count()


class ProjectFile(BaseModelMixin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="project_files/", validators=[validate_file_size])
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, blank=True)
    size = models.PositiveIntegerField(help_text="File size in bytes", default=0)
    

    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size
            self.file_type = (
                self.file.name.split(".")[-1] if "." in self.file.name else ""
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.project.name})"


class EmbeddingData(BaseModelMixin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    embedding = VectorField(dimensions=768, null=True)


class Chat(BaseModelMixin):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
