
from django.core.management.base import BaseCommand

from apps.projects.models import ProjectReminder
from apps.projects.services import send_project_reminder


class Command(BaseCommand):
    help = "Αποστολή υπενθυμίσεων για έντυπα έργων."

    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                "=== ΕΛΕΓΧΟΣ ΥΠΕΝΘΥΜΙΣΕΩΝ ΕΡΓΩΝ ==="
            )
        )
        self.stdout.write("")

        reminders = (
            ProjectReminder.objects
            .select_related(
                "document",
                "document__project",
                "document__responsible",
                "document__project__responsible",
            )
            .all()
            .order_by("document__due_date", "days_before")
        )

        total = reminders.count()

        sent = 0
        skipped = 0
        errors = 0

        self.stdout.write(
            f"Σύνολο reminders: {total}"
        )
        self.stdout.write("")

        for reminder in reminders:

            document = reminder.document
            project = document.project

            self.stdout.write("-" * 70)

            self.stdout.write(
                f"Reminder: {reminder.id}"
            )

            self.stdout.write(
                f"Έργο: {project.title}"
            )

            self.stdout.write(
                f"Έντυπο: {document.title}"
            )

            self.stdout.write(
                f"Ημερομηνία παράδοσης: "
                f"{document.due_date:%d/%m/%Y}"
            )

            self.stdout.write(
                f"Ημέρες πριν: {reminder.days_before}"
            )

            self.stdout.write(
                f"Ημερομηνία reminder: "
                f"{reminder.reminder_date:%d/%m/%Y}"
            )

            self.stdout.write(
                f"Ενεργό: {reminder.is_active}"
            )

            self.stdout.write(
                f"Sent at: {reminder.sent_at}"
            )

            self.stdout.write(
                f"Υποβλήθηκε: {document.submitted}"
            )

            # --------------------------------------------------
            # Έλεγχος 1: Ενεργό reminder
            # --------------------------------------------------

            if not reminder.is_active:

                self.stdout.write(
                    self.style.WARNING(
                        "⏭ ΠΑΡΑΛΕΙΨΗ: Το reminder είναι ανενεργό."
                    )
                )

                skipped += 1
                continue

            # --------------------------------------------------
            # Έλεγχος 2: Έχει ήδη σταλεί
            # --------------------------------------------------

            if reminder.sent_at is not None:

                self.stdout.write(
                    self.style.WARNING(
                        "⏭ ΠΑΡΑΛΕΙΨΗ: Το reminder έχει ήδη σταλεί."
                    )
                )

                skipped += 1
                continue

            # --------------------------------------------------
            # Έλεγχος 3: Έχει υποβληθεί το έντυπο
            # --------------------------------------------------

            if document.submitted:

                self.stdout.write(
                    self.style.WARNING(
                        "⏭ ΠΑΡΑΛΕΙΨΗ: Το έντυπο έχει ήδη υποβληθεί."
                    )
                )

                skipped += 1
                continue

            # --------------------------------------------------
            # Έλεγχος 4: Η ημερομηνία reminder
            # --------------------------------------------------

            if not reminder.should_send:

                self.stdout.write(
                    self.style.WARNING(
                        "⏭ ΠΑΡΑΛΕΙΨΗ: Δεν έχει έρθει ακόμα "
                        "η ημερομηνία αποστολής."
                    )
                )

                skipped += 1
                continue

            # --------------------------------------------------
            # Βρες υπεύθυνο
            # --------------------------------------------------

            recipient = (
                document.responsible
                or project.responsible
            )

            if not recipient:

                self.stdout.write(
                    self.style.ERROR(
                        "❌ ΠΑΡΑΛΕΙΨΗ: Δεν υπάρχει υπεύθυνος "
                        "ούτε στο έντυπο ούτε στο έργο."
                    )
                )

                skipped += 1
                continue

            self.stdout.write(
                f"Υπεύθυνος: {recipient}"
            )

            # --------------------------------------------------
            # Έλεγχος email
            # --------------------------------------------------

            if not recipient.email:

                self.stdout.write(
                    self.style.ERROR(
                        "❌ ΠΑΡΑΛΕΙΨΗ: Ο υπεύθυνος δεν έχει email."
                    )
                )

                skipped += 1
                continue

            self.stdout.write(
                f"Email: {recipient.email}"
            )

            # --------------------------------------------------
            # Αποστολή
            # --------------------------------------------------

            self.stdout.write(
                "📧 Προσπάθεια αποστολής..."
            )

            try:

                result = send_project_reminder(reminder)

                if result:

                    self.stdout.write(
                        self.style.SUCCESS(
                            "✅ ΕΣΤΑΛΗ ΕΠΙΤΥΧΩΣ"
                        )
                    )

                    sent += 1

                else:

                    self.stdout.write(
                        self.style.WARNING(
                            "⚠️ Δεν στάλθηκε "
                            "(το service επέστρεψε False)."
                        )
                    )

                    skipped += 1

            except Exception as exc:

                self.stdout.write(
                    self.style.ERROR(
                        f"❌ ERROR: {exc}"
                    )
                )

                errors += 1

        # ------------------------------------------------------
        # Σύνοψη
        # ------------------------------------------------------

        self.stdout.write("")
        self.stdout.write("=" * 70)

        self.stdout.write(
            self.style.SUCCESS(
                f"Απεστάλησαν: {sent}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"Παραλείφθηκαν: {skipped}"
            )
        )

        self.stdout.write(
            self.style.ERROR(
                f"Σφάλματα: {errors}"
            )
        )

        self.stdout.write(
            f"Σύνολο: {total}"
        )

        self.stdout.write("=" * 70)
        self.stdout.write("")
