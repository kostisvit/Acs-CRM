import csv
from apps.organizations.models import Organization
from apps.parameters.models import JobType, OtsSoftware

def str_to_bool(value):
    return str(value).strip().lower() in ("true", "1", "yes", "y")


class BaseImporter:
    model = None

    def import_file(self, csv_file):
        decoded = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded)

        imported = 0
        errors = []

        for line, row in enumerate(reader, start=2):
            try:
                self.import_row(row)
                imported += 1

            except Exception as e:
                errors.append(f"Line {line}: {e}")

        return imported, errors

    def import_row(self, row):
        raise NotImplementedError
    
  
  
  
class CustomerImporter(BaseImporter):
    model = Organization

    def import_row(self, row):
        self.model.objects.update_or_create(
            org_name=row["name"],
            defaults={
                "org_address": row["address"],
                "org_city": row["city"],
                "org_phone": row["phone"],
                "org_remote": row["teamviewer"],
                "org_email": row["email"],
                "org_site": row["website"],
                "org_info": row["info"],
                "is_visible": str_to_bool(row["is_visible"]),
            },
        )

class JobTypeImporter(BaseImporter):
    model = JobType

    def import_row(self, row):
        self.model.objects.update_or_create(
            name=row["name"],
            defaults={
                "is_active": str_to_bool(row["is_active"]),
            },
        )


class OtsSoftwareImporter(BaseImporter):
    model = OtsSoftware

    def import_row(self, row):
        self.model.objects.update_or_create(
            name=row["name"],
            defaults={
                "is_active": str_to_bool(row["is_active"]),
            },
        )

IMPORTERS = {
    "customers": {
        "class": CustomerImporter,
        "label": "Οργανισμοί",
    },
    "job_types": {
        "class": JobTypeImporter,
        "label": "Τύποι Εργασίας",
    },
    "ots_software": {
        "class": OtsSoftwareImporter,
        "label": "Λογισμικό OTS",
    },
}