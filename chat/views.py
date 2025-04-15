import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from pgvector.django import L2Distance

from chat.prompts import CHAT_PROMPT as prompt
from config.settings import llm
from config.utils.embedding import extract_text_from_pdf, get_embeddings

from .models import Chat, EmbeddingData, Project, ProjectFile


class HomeView(View):
    def get(self, request):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            projects = Project.objects.filter(is_deleted=False).order_by("-created_at")
            return JsonResponse(
                {
                    "projects": [
                        {
                            "id": p.id,
                            "name": p.name,
                            "description": p.description,
                            "created_at": p.created_at.isoformat(),
                            "files": [
                                {
                                    "id": f.id,
                                    "name": f.name,
                                    "file_type": f.file_type,
                                    "size": f.size,
                                    "created_at": f.created_at.isoformat(),
                                }
                                for f in p.files.filter(is_deleted=False)
                            ],
                        }
                        for p in projects
                    ]
                }
            )
        return self.render_to_response({})

    def render_to_response(self, context):
        return TemplateView.render_to_response(self, context, template_name="home.html")


class CreateProjectView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            project = Project.objects.create(
                name=data["name"], description=data.get("description", "")
            )
            return JsonResponse(
                {
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "slug": project.slug,
                    "created_at": project.created_at.isoformat(),
                }
            )
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"error": "Invalid request"}, status=400)


class UpdateProjectView(View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        try:
            data = json.loads(request.body)
            project.name = data["name"]
            project.description = data.get("description", project.description)
            project.save()
            return JsonResponse(
                {
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "slug": project.slug,
                    "updated_at": project.updated_at.isoformat(),
                }
            )
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"error": "Invalid request"}, status=400)


class DeleteProjectView(View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        project.is_deleted = True
        project.save()
        return JsonResponse({"success": True})


class UploadFileView(View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        file = request.FILES.get("file")

        if not file:
            return JsonResponse({"error": "No file was uploaded"}, status=400)

        if file.content_type != "application/pdf":
            return JsonResponse({"error": "Only PDF files are allowed"}, status=400)

        if file.size > 10 * 1024 * 1024:  # 10MB
            return JsonResponse({"error": "File size must not exceed 10MB"}, status=400)

        try:
            name = request.POST.get("name", file.name)
            project_file = ProjectFile.objects.create(
                project=project, file=file, name=name
            )
            # Extract text from PDF
            pdf_text = extract_text_from_pdf(project_file.file.path)
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            chunks = text_splitter.split_text(pdf_text)

            embedding_data = []
            if chunks:
                embeddings = get_embeddings(chunks)
                for chunk, embedding in zip(chunks, embeddings):
                    embedding_data.append(
                        EmbeddingData(
                            project=project,
                            content=chunk,
                            embedding=embedding,
                        )
                    )
                EmbeddingData.objects.bulk_create(embedding_data, ignore_conflicts=True)

            return JsonResponse(
                {
                    "id": project_file.id,
                    "name": project_file.name,
                    "file_type": project_file.file_type,
                    "size": project_file.size,
                    "created_at": project_file.created_at.isoformat(),
                }
            )
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": f"Failed to upload file: {str(e)}"}, status=500
            )


class DeleteFileView(View):
    def post(self, request, file_id):
        project_file = get_object_or_404(ProjectFile, id=file_id)
        project_file.is_deleted = True
        project_file.save()
        return JsonResponse({"success": True})


class ProjectFilesView(View):
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        files = project.files.filter(is_deleted=False).order_by("-created_at")

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "files": [
                        {
                            "id": f.id,
                            "name": f.name,
                            "file_type": f.file_type,
                            "size": f.size,
                            "created_at": f.created_at.isoformat(),
                        }
                        for f in files
                    ]
                }
            )
        return self.render_to_response({"project": project, "files": files})

    def render_to_response(self, context):
        return TemplateView.render_to_response(
            self, context, template_name="project_files.html"
        )


class ProjectChatView(TemplateView):
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = get_object_or_404(Project, id=kwargs["project_id"])
        context["project"] = project
        context["files"] = project.files.filter(is_deleted=False).order_by(
            "-created_at"
        )
        return context


class GetChatHistoryView(View):
    def get(self, request, project_id):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            project = get_object_or_404(Project, id=project_id)
            chats = Chat.objects.filter(project=project).order_by("id")
            return JsonResponse(
                {
                    "chats": [
                        {
                            "id": c.id,
                            "message": c.message,
                            "response": c.response,
                            "created_at": c.created_at.isoformat(),
                        }
                        for c in chats
                    ]
                }
            )
        return JsonResponse({"error": "Invalid request"}, status=400)


class SendChatMessageView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            project_id = data["project_id"]
            message = data["message"]
            semantic_search = (
                EmbeddingData.objects.filter(project_id=project_id)
                .annotate(distance=L2Distance("embedding", get_embeddings(message)[0]))
                .order_by("-distance")
            )

            project_file = semantic_search.first()
            if not project_file:
                return JsonResponse({"error": "No relevant context found"}, status=400)

            chain = prompt | llm | StrOutputParser()
            result = chain.invoke(
                {"context": project_file.content, "question": message}
            )

            chat = Chat.objects.create(
                project=project_file.project,
                message=message,
                response=result,
            )

            return JsonResponse({"response": chat.response})

        except (json.JSONDecodeError, KeyError) as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
