from django.urls import path

from chat import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("projects/create/", views.CreateProjectView.as_view(), name="create_project"),
    path(
        "projects/<int:project_id>/update/",
        views.UpdateProjectView.as_view(),
        name="update_project",
    ),
    path(
        "projects/<int:project_id>/delete/",
        views.DeleteProjectView.as_view(),
        name="delete_project",
    ),
    path(
        "projects/<int:project_id>/upload/",
        views.UploadFileView.as_view(),
        name="upload_file",
    ),
    path(
        "projects/<int:project_id>/files/",
        views.ProjectFilesView.as_view(),
        name="get_project_files",
    ),
    path(
        "files/<int:file_id>/delete/",
        views.DeleteFileView.as_view(),
        name="delete_file",
    ),
    path(
        "projects/<int:project_id>/chat/",
        views.ProjectChatView.as_view(),
        name="project_chat",
    ),
    path(
        "chat/send/",
        views.SendChatMessageView.as_view(),
        name="send_chat_message",
    ),
    path(
        "projects/<int:project_id>/chat/history/",
        views.GetChatHistoryView.as_view(),
        name="get_chat_history",
    ),
]
