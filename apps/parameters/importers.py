import csv
from apps.organizations.models import Organization, Employee
from apps.parameters.models import JobType, OtsSoftware, OrgDepartment, AcsAdeia
from abc import ABC, abstractmethod

def str_to_bool(value):
    return str(value).strip().lower() in ("true", "1", "yes", "y")


class BaseImporter(ABC):

    model = None

    @abstractmethod
    def import_row(self, row):
        """
        Import a single CSV row.
        Must be implemented by subclasses.
        """
        pass

    def import_file(self, csv_file):
        imported = 0
        errors = []
        csv_records = 0

        csv_file.seek(0)

        decoded = csv_file.read().decode("utf-8-sig")
        reader = csv.DictReader(decoded.splitlines())

        for row_number, row in enumerate(reader, start=2):
            csv_records += 1

            try:
                self.import_row(row)
                imported += 1

            except Exception as e:
                errors.append({
                    "row": row_number,
                    "error": str(e),
                    "data": row,
                })

        return {
            "imported": imported,
            "csv_records": csv_records,
            "errors": errors,
        }
    
  
  
  
class OrganizationImporter(BaseImporter):
    model = Organization

    def import_row(self, row):
        self.model.objects.update_or_create(
            source_id=row["id"],
            defaults={
                "org_name": row["name"],
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


class EmployeeImporter(BaseImporter):
    model = Employee

    def import_row(self, row):
        department = None

        if row.get("org_department"):
            department = OrgDepartment.objects.filter(
                source_id=row["org_department"].strip()
            ).first()

            if not department:
                raise ValueError(
                    f"Department not found: {row['org_department']}"
                )

        organization = None

        if row.get("dhmos"):
            organization = Organization.objects.filter(
                source_id=row["dhmos"].strip()
            ).first()

            if not organization:
                raise ValueError(
                    f"Missing organization source id: {row['dhmos']}"
                )

        email = row.get("email", "").strip().lower()

        if not email:
            email = f"employee-{row['id']}@invalid.local"

        self.model.objects.update_or_create(
            email=email,
            defaults={
                "organization": organization,
                "firstname": row.get("firstname", ""),
                "lastname": row.get("lastname", ""),
                "phone": row.get("phone", ""),
                "cellphone": row.get("cellphone", ""),
                "secondary_email": row.get("secondary_email", ""),
                "info": row.get("info", ""),
                "is_active": str_to_bool(row.get("is_visible", "")),
                "org_department": department,
            }
        )

        return True


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


class OrgDepartmentImporter(BaseImporter):
    model = OrgDepartment

    def import_row(self, row):
        self.model.objects.update_or_create(
            source_id=row["id"],
            name=row["name"],
            defaults={
                "is_active": str_to_bool(row["is_active"]),
            },
        )


class AcsAdeiaTypeImporter(BaseImporter):
    model = AcsAdeia

    def import_row(self, row):
        self.model.objects.update_or_create(
            source_id=row["id"],
            name=row["name"],
            adeianame_id=row["adeianame_id"],
            defaults={
                "is_active": str_to_bool(row["is_active"]),
            },
            
        )

IMPORTERS = {
    "customers": {
        "class": OrganizationImporter,
        "label": "Οργανισμοί",
    },
    "employees": {
        "class": EmployeeImporter,
        "label": "Επαφές Οργανισμών",
    },
    "job_types": {
        "class": JobTypeImporter,
        "label": "Τύποι Εργασίας",
    },
    "ots_software": {
        "class": OtsSoftwareImporter,
        "label": "Λογισμικό OTS",
    },
    "org_department": {
        "class": OrgDepartmentImporter,
        "label": "Διευθύνσεις Οργανισμού",
    },
    "acsadeiatype": {
        "class": AcsAdeiaTypeImporter,
        "label": "Είδος άδειας"
    }
}