from django.urls import path

from . import views

app_name = "projects"


urlpatterns = [
    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "projects/",
        views.project_list,
        name="project_list",
    ),

    path(
        "projects/new/",
        views.project_create,
        name="project_create",
    ),

    path(
        "projects/<uuid:pk>/",
        views.project_detail,
        name="project_detail",
    ),

    path(
        "projects/<uuid:pk>/edit/",
        views.project_edit,
        name="project_edit",
    ),

    path(
        "projects/<uuid:project_pk>/documents/new/",
        views.document_create,
        name="document_create",
    ),

    path(
        "documents/<uuid:pk>/submit/",
        views.document_submit,
        name="document_submit",
    ),
]
