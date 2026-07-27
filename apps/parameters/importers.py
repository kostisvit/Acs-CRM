import csv
from apps.organizations.models import Organization, Employee, Tasks
from apps.parameters.models import JobType, OtsSoftware, OrgDepartment, AcsAdeia
from abc import ABC, abstractmethod
from decimal import Decimal
from django.contrib.auth import get_user_model
from decimal import InvalidOperation


User = get_user_model()

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
                "is_active": str_to_bool(row["is_visible"]),
                "created": row["created"],
                "modified": row["modified"],
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

        source_id = row.get("id", "").strip()

        email = row.get("email", "").strip().lower()

        if not email:
            email = f"employee-{source_id}@invalid.local"

        self.model.objects.update_or_create(
            source_id=source_id,   # lookup field
            defaults={
                "email": email,
                "organization": organization,
                "firstname": row.get("firstname", ""),
                "lastname": row.get("lastname", ""),
                "phone": row.get("phone", ""),
                "cellphone": row.get("cellphone", ""),
                "secondary_email": row.get("secondary_email", ""),
                "info": row.get("info", ""),
                "is_active": str_to_bool(row.get("is_visible", "")),
                "org_department": department,
                "created": row["created"],
                "modified": row["modified"],
            }
        )

        return True


class JobTypeImporter(BaseImporter):
    model = JobType

    def import_row(self, row):
        self.model.objects.update_or_create(
            source_id=row["id"],
            defaults={
                "name":row["name"],
                "is_active": str_to_bool(row["is_active"]),
                "created": row["created"],
                "modified": row["modified"],
            },
        )


class OtsSoftwareImporter(BaseImporter):
    model = OtsSoftware

    def import_row(self, row):
        self.model.objects.update_or_create(
            source_id=row["id"],
            defaults={
                "name": row["name"],
                "is_active": str_to_bool(row["is_active"]),
                "created": row["created"],
                "modified": row["modified"],
                
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
                "created": row["created"],
                "modified": row["modified"],
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
                "created": row["created"],
                "modified": row["modified"],
            },
            
        )






class TaskImporter(BaseImporter):
    model = Tasks

    def import_row(self, row):

        # Organization (your model has org_name)
        organization = Organization.objects.filter(
            org_name=row["dhmos"].strip()
        ).first()

        if organization is None:
            raise ValueError(
                f"Missing organization: {row['dhmos']}"
            )

        job_type_acs = None

        if row.get("job_type_acs") and row["job_type_acs"].strip():
            job_type_acs = JobType.objects.filter(
                source_id=int(row["job_type_acs"].strip())
            ).first()

            if not job_type_acs:
                raise ValueError(
                    f"Job type not found: {row['job_type_acs']}"
                )

        # OtsSoftware does NOT have source_id, use id
        org_app = None
        if row.get("org_app") and row["org_app"].strip():
            org_app = OtsSoftware.objects.filter(
                source_id=int(row["org_app"])
            ).first()

        # Employee does NOT have source_id, use id
        org_employee = None
        if row.get("org_employee") and row["org_employee"].strip():
            org_employee = Employee.objects.filter(
                source_id=int(row["org_employee"])
            ).first()

        # ACS User uses email, not username
        employee_code = row.get("employee", "").strip()

        if not employee_code:
            raise ValueError("Missing ACS employee")

        email = employee_code
        if "@" not in email:
            email = f"{email}@acsservices.gr"

        acs_employee, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": employee_code,
                "is_active": True,
            }
        )

        if created:
            acs_employee.set_unusable_password()
            acs_employee.save()

        # Convert time safely
        try:
            task_time = Decimal(
                row["time"].replace(",", ".")
            )
        except (InvalidOperation, AttributeError):
            raise ValueError(
                f"Invalid task time: {row.get('time')}"
            )

        self.model.objects.update_or_create(
            source_id=row["id"],
            defaults={
                "organization": organization,
                "importdate": row["importdate"],
                "org_app": org_app,
                "job_type_acs": job_type_acs,
                "task_info": row["info"],
                "task_note": row.get("text", ""),
                "acs_employee": acs_employee,
                "task_time": task_time,
                "org_employee": org_employee,
                "ticketid": row.get("ticketid") or f"IMPORT-{row['id']}",
                "created": row["created"],
                "modified": row["modified"],
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
    },
    "tasks":{
        "class": TaskImporter,
        "label": "Εργασίες"
    }
}