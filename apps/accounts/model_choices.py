type_choice = (
    ('laptop', 'Laptop'),
    ('desktop', 'Desktop'),
    ('tameiakh', 'Ταμειακή Μηχανή'),
)

tmhma_choice = (
    ('1', 'Οικονομική'),
    ('2', 'Τεχνική'),
    ('3', 'Διοικητική'),
    ('4', 'Γραφείο Προσωπικού'),
    ('5', 'Μισθοδοσία'),
    ('6', 'Γραφείο Δημάρχου'),
    ('7', 'Τμήμα Πληροφορικής'),
    ('8', 'Ληξιαρχείο'),
    ('9', 'Αντιδήμαρχος'),
    ('10', 'Γραφείο Κίνησης'),
    ('11', 'Δήμαρχος'),
    ('12', 'Γενικός Γραμματέας'),
    ('13', 'Υπηρεσία Καθαριότητας'),
    ('14', 'Γραφείο Πρωτοκόλλου'),
    ('15', 'Ειδικός Συνεργάτης')
)

job_choice = (
    ('TeamViewer', 'TeamViewer'),
    ('Επίσκεψη', 'Επίσκεψη'),
    ('Γραφείο', 'Γραφείο'),
    ('Webinar-Zoom', 'Webinar-Zoom')
)

from django.db import models

adeia_choice = (
    ('1', 'Κανονική'),
    ('2', 'Αναρρωτική'),
    ('3', 'Εορταστική')
)

app_choice = (
    ('ΤΑΠ', 'ΤΑΠ'),
    ('Μισθοδοσία', 'Μισθοδοσία'),
    ('Διαχείριση Προσωπικού', 'Διαχείριση Προσωπικού'),
    ('Διαχείριση Μισθωμάτων', 'Διαχείριση Μισθωμάτων'),
    ('Λογιστική', 'Λογιστική'),
    ('Μητρώο Πολιτών', 'Μητρώο Πολιτών'),
    ('Ύδρευση', 'Ύδρευση'),
    ('Αποφάσεις', 'Αποφάσεις'),
    ('Πρωτόκολλο', 'Πρωτόκολλο'),
    ('Γραφείο Κίνησης', 'Γραφείο Κίνησης'),
    ('Διαύγεια', 'Διαύγεια'),
    ('Έσοδα', 'Έσοδα'),
    ('Κοιμητήρια', 'Κοιμητήρια'),
    ('ΚΟΚ', 'ΚΟΚ'),
    ('Δημοτικός φόρος', 'Δημοτικός φόρος'),
    ('Site', 'Site'),
    ('Web Άδειες','Web Άδειες'),
    ('Πρακτικό', 'Πρακτικό'),
    ('Hardware', 'Hardware'),
    ('Ύδατα', 'Ύδατα'),
    ('OPEN1|Process', 'OPEN1|Process'),
    ('OPEN1|Fin', 'OPEN1|Fin'),
    ('OPEN1|HR', 'OPEN1|HR'),
    ('OPEN1|Property', 'OPEN1|Property'),
    ('Open1|Decisions','Open1|Decisions'),
    ('Open1|Entrance', 'Open1|Entrance'),
    ('OPEN1|Fleet', 'OPEN1|Fleet'),
    ('OPEN1|Project360','OPEN1|Project360'),
    ('4myCity', '4myCity'),
    ('Easy Pay', 'EasyPay'),
    ('Εσωτερικός Έλεγχος-Επιχ. Συν.', 'Εσωτερικός Έλεγχος-Επιχ. Συν.'),
    ('Ηλεκτ.Εισπρ. ΔΙΑΣ', 'Ηλεκτ.Εισπρ. ΔΙΑΣ'),
    ('Διαχείριση Ποιότητας - ISO', 'Διαχείριση Ποιότητας - ISO'),

)

pc_brand_choice = (
    ('HP', 'HP'),
    ('Fujitsu', 'Fujitsu'),
    ('Acer', 'Acer'),
    ('Lenovo', 'Lenovo'),
    ('Custom', 'Custom')
)

polisi_choice = (
    ('OPEN', 'OPEN'),
    ('CLOSED', 'CLOSED')
)

class TrainingChoice(models.TextChoices):
    OTS = '1', 'OTS'
    ACS = '2', 'ACS'
    
training_choice = (
    ('Εκπαίδευση', 'Εκπαίδευση'),
)

training_place = (
    ('Remote', 'Remote'),
    ('Γραφεία OTS', 'Γραφεία OTS'),
    ('Γραφείο ACS', 'Γραφείο ACS')
)

software_type = (
        ('Antivirus','Antivirus'),
        ('Solidus-Vertigo','Solidus-Vertigo'),
        ('Office 365', 'Office 365'),
        ('Remote', 'Remote')
    )