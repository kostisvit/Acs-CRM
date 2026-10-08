from django.conf import settings
from django.core.mail import send_mail


def send_project_reminder(reminder):
    """
    Στέλνει email υπενθύμισης για ένα ProjectDocument.

    Προτεραιότητα παραλήπτη:
    1. Υπεύθυνος εντύπου
    2. Υπεύθυνος έργου
    """

    document = reminder.document
    project = document.project

    # Πρώτα ο υπεύθυνος του εντύπου,
    # διαφορετικά ο υπεύθυνος του έργου.
    recipient = (
        document.responsible
        or project.responsible
    )

    # Δεν υπάρχει παραλήπτης.
    if not recipient or not recipient.email:
        return False

    # Subject
    if reminder.days_before == 0:
        subject = (
            f"Προθεσμία σήμερα: {document.title}"
        )
    elif reminder.days_before == 1:
        subject = (
            f"Υπενθύμιση: {document.title} "
            f"λήγει αύριο"
        )
    else:
        subject = (
            f"Υπενθύμιση: {document.title} "
            f"σε {reminder.days_before} ημέρες"
        )

    # Email body
    message = (
        f"Έχετε μια εκκρεμή υποχρέωση για το έργο:\n\n"
        f"Έργο: {project.title}\n"
        f"Έντυπο: {document.title}\n"
        f"Ημερομηνία παράδοσης: "
        f"{document.due_date:%d/%m/%Y}\n\n"
        f"Παρακαλούμε να ολοκληρώσετε και να υποβάλετε "
        f"το έντυπο μέχρι την παραπάνω ημερομηνία."
    )

    # Αποστολή email
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient.email],
        fail_silently=False,
    )

    # Μόνο αφού σταλεί επιτυχώς,
    # μαρκάρουμε το reminder ως απεσταλμένο.
    reminder.mark_as_sent()

    return True
