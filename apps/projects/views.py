from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ProjectDocumentForm, ProjectDocumentSubmitForm, ProjectForm
from .models import Project, ProjectDocument


@login_required
def dashboard(request):
    today = timezone.localdate()

    projects = Project.objects.filter(
        is_active=True
    ).select_related(
        "organization",
        "responsible",
    )

    documents = ProjectDocument.objects.filter(
        submitted=False
    ).select_related(
        "project",
        "project__organization",
        "responsible",
    )

    overdue_documents = documents.filter(
        due_date__lt=today
    ).order_by("due_date")

    due_today = documents.filter(
        due_date=today
    ).order_by("due_date")

    upcoming_documents = documents.filter(
        due_date__gt=today,
        due_date__lte=today + timezone.timedelta(days=7),
    ).order_by("due_date")

    context = {
        "projects_count": projects.count(),

        "documents_count": ProjectDocument.objects.count(),

        "pending_documents_count": documents.count(),

        "overdue_count": overdue_documents.count(),

        "due_today_count": due_today.count(),

        "upcoming_count": upcoming_documents.count(),

        "overdue_documents": overdue_documents[:10],

        "due_today": due_today[:10],

        "upcoming_documents": upcoming_documents[:10],

        "projects": projects[:10],
    }

    return render(
        request,
        "projects/dashboard.html",
        context,
    )


@login_required
def project_list(request):
    projects = (
        Project.objects
        .select_related(
            "organization",
            "responsible",
        )
        .annotate(
            documents_total=Count("documents"),
            documents_completed=Count(
                "documents",
                filter=Q(documents__submitted=True),
            ),
        )
    )

    search = request.GET.get("q", "").strip()

    if search:
        projects = projects.filter(
            Q(title__icontains=search)
            | Q(
                organization__org_name__icontains=search
            )
        )

    status = request.GET.get("status")

    if status == "active":
        projects = projects.filter(is_active=True)

    elif status == "inactive":
        projects = projects.filter(is_active=False)

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects,
            "search": search,
            "status": status,
        },
    )


@login_required
def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.select_related(
            "organization",
            "responsible",
        ),
        pk=pk,
    )

    documents = (
        project.documents
        .select_related("responsible")
        .order_by("due_date")
    )

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
            "documents": documents,
        },
    )


@login_required
def project_create(request):

    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save()

            messages.success(
                request,
                "Το έργο δημιουργήθηκε επιτυχώς.",
            )

            return redirect(
                "projects:project_detail",
                pk=project.pk,
            )

    else:
        form = ProjectForm()

    return render(
        request,
        "projects/project_form.html",
        {
            "form": form,
            "title": "Νέο έργο",
        },
    )


@login_required
def project_edit(request, pk):

    project = get_object_or_404(
        Project,
        pk=pk,
    )

    if request.method == "POST":
        form = ProjectForm(
            request.POST,
            instance=project,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Το έργο ενημερώθηκε επιτυχώς.",
            )

            return redirect(
                "projects:project_detail",
                pk=project.pk,
            )

    else:
        form = ProjectForm(
            instance=project,
        )

    return render(
        request,
        "projects/project_form.html",
        {
            "form": form,
            "project": project,
            "title": "Επεξεργασία έργου",
        },
    )


@login_required
def document_create(request, project_pk):

    project = get_object_or_404(
        Project,
        pk=project_pk,
    )

    if request.method == "POST":
        form = ProjectDocumentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            document = form.save(commit=False)

            document.project = project

            document.submitted = False
            document.submitted_at = None

            document.save()

            document.create_default_reminders()

            messages.success(
                request,
                "Το έντυπο δημιουργήθηκε επιτυχώς.",
            )

            return redirect(
                "projects:project_detail",
                pk=project.pk,
            )

    else:
        form = ProjectDocumentForm()

    return render(
        request,
        "projects/document_form.html",
        {
            "form": form,
            "project": project,
            "title": "Ανέβασμα εγγράφου",
        },
    )


@login_required
def document_submit(request, pk):

    document = get_object_or_404(
        ProjectDocument,
        pk=pk,
    )

    if document.submitted:
        messages.info(
            request,
            "Το έντυπο έχει ήδη υποβληθεί.",
        )

        return redirect(
            "projects:project_detail",
            pk=document.project.pk,
        )

    if request.method == "POST":

        form = ProjectDocumentSubmitForm(
            request.POST,
            request.FILES,
            instance=document,
        )

        if form.is_valid():

            document.file = form.cleaned_data["file"]
            document.submitted = True
            document.submitted_at = timezone.now()

            document.save(
                update_fields=[
                    "file",
                    "submitted",
                    "submitted_at",
                    "modified",
                ]
            )

            messages.success(
                request,
                "Το έντυπο υποβλήθηκε επιτυχώς.",
            )

            return redirect(
                "projects:project_detail",
                pk=document.project.pk,
            )

    else:
        form = ProjectDocumentSubmitForm(
            instance=document,
        )

    return render(
        request,
        "projects/document_submit.html",
        {
            "form": form,
            "document": document,
            "project": document.project,
        },
    )
