
from django.contrib import admin

from .models import Project, ProjectDocument, ProjectReminder


class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 0
    show_change_link = True

    fields = (
        "title",
        "due_date",
        "responsible",
        "submitted",
        "submitted_at",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organization",
        "responsible",
        "start_date",
        "end_date",
        "is_active",
        "documents_status",
    )

    list_filter = (
        "is_active",
        "organization",
    )

    search_fields = (
        "title",
        "description",
        "organization__org_name",
        "responsible__username",
        "responsible__first_name",
        "responsible__last_name",
    )

    autocomplete_fields = (
        "organization",
        "responsible",
    )

    date_hierarchy = "start_date"

    readonly_fields = (
        "created",
        "modified",
    )

    inlines = (
        ProjectDocumentInline,
    )

    fieldsets = (
        (
            "Βασικές πληροφορίες",
            {
                "fields": (
                    "organization",
                    "title",
                    "description",
                )
            },
        ),
        (
            "Ημερομηνίες",
            {
                "fields": (
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            "Υπεύθυνος",
            {
                "fields": (
                    "responsible",
                )
            },
        ),
        (
            "Κατάσταση",
            {
                "fields": (
                    "is_active",
                    "info",
                )
            },
        ),
        (
            "Σύστημα",
            {
                "fields": (
                    "created",
                    "modified",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Έντυπα")
    def documents_status(self, obj):
        total = obj.documents.count()
        completed = obj.completed_documents_count
        overdue = obj.overdue_documents_count

        if overdue:
            return f"⚠ {completed}/{total} — {overdue} εκπρόθεσμα"

        return f"{completed}/{total}"


@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "organization",
        "due_date",
        "responsible",
        "submitted",
        "status_display",
    )

    list_filter = (
        "submitted",
        "project__organization",
        "due_date",
    )

    search_fields = (
        "title",
        "description",
        "project__title",
        "project__organization__org_name",
        "responsible__username",
        "responsible__first_name",
        "responsible__last_name",
    )

    autocomplete_fields = (
        "project",
        "responsible",
    )

    date_hierarchy = "due_date"

    readonly_fields = (
        "created",
        "modified",
        "submitted_at",
    )

    fieldsets = (
        (
            "Έντυπο",
            {
                "fields": (
                    "project",
                    "title",
                    "description",
                )
            },
        ),
        (
            "Προθεσμία",
            {
                "fields": (
                    "due_date",
                    "responsible",
                )
            },
        ),
        (
            "Υποβολή",
            {
                "fields": (
                    "submitted",
                    "submitted_at",
                    "file",
                )
            },
        ),
        (
            "Σημειώσεις",
            {
                "fields": (
                    "notes",
                )
            },
        ),
        (
            "Σύστημα",
            {
                "fields": (
                    "created",
                    "modified",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Οργανισμός")
    def organization(self, obj):
        return obj.project.organization

    @admin.display(description="Κατάσταση")
    def status_display(self, obj):
        statuses = {
            "submitted": "✓ Υποβλήθηκε",
            "overdue": "🔴 Εκπρόθεσμο",
            "due_today": "🔴 Λήγει σήμερα",
            "urgent": "🟠 Επείγον",
            "warning": "🟡 Πλησιάζει",
            "pending": "🟢 Εκκρεμεί",
        }

        return statuses.get(obj.status, obj.status)


@admin.register(ProjectReminder)
class ProjectReminderAdmin(admin.ModelAdmin):
    list_display = (
        "document",
        "days_before",
        "reminder_date_display",
        "is_active",
        "sent_at",
    )

    list_filter = (
        "is_active",
        "sent_at",
        "days_before",
    )

    search_fields = (
        "document__title",
        "document__project__title",
        "document__project__organization__org_name",
    )

    autocomplete_fields = (
        "document",
    )

    readonly_fields = (
        "sent_at",
        "created",
        "modified",
    )

    @admin.display(description="Ημερομηνία υπενθύμισης")
    def reminder_date_display(self, obj):
        return obj.reminder_date
