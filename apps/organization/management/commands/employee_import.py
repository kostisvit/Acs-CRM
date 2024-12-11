import csv
import time
import sys
from django.core.management import BaseCommand
from organization.models import Employee, Organization

class Command(BaseCommand):
    help = "Load Employees from CSV into the database"

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        start_time = time.time()
        path = kwargs['path']

        if not path:
            self.stderr.write("Please provide a valid path to the CSV file using the --path argument.")
            sys.exit(1)

        try:
            with open(path, 'rt', encoding='utf-8-sig') as f:
                reader = csv.reader(f, dialect='excel', delimiter=',', quotechar='"')
                header = next(reader, None)  # Skip the header row

                if not header:
                    self.stderr.write("The CSV file is empty or missing a header row.")
                    sys.exit(1)

                for row_num, row in enumerate(reader, start=1):
                    try:
                        if len(row) < 4:  # Ensure there are enough columns
                            raise ValueError("Row does not contain the required number of columns.")

                        Employee.objects.update_or_create(
                            old_id=row[0],
                            organization = Organization.objects.get(old_id=row[1]),
                            defaults={
                                # 'organization': row[1],
                                'firstname': row[2],
                                'lastname': row[3],
                                'tmhma': row[4],
                                'phone': row[5],
                                'cellphone': row[6],
                                'email': row[7],
                                'secondary_email': row[8],
                                'info': row[9],
                                'is_visible': row[10],
                            }
                        )

                    except Exception as err:
                        with open('errors.csv', 'a', encoding='utf-8-sig') as error_file:
                            error_writer = csv.writer(error_file, delimiter=',', quotechar='"')
                            if row_num == 1:  # Write header only once
                                error_writer.writerow(['row_num', 'organization', 'firstname', 'lastname', 'tmhma','phone','cellphone','email','secondary_email','info','is_visible', 'error'])
                            error_writer.writerow([row_num] + row + [str(err)])
                        self.stderr.write(f"Invalid data in row {row_num}. Skipping...")
                        self.stderr.write(f"Row: {row}, Reason: {err}")

        except FileNotFoundError:
            self.stderr.write(f"File not found: {path}")
            sys.exit(1)
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {e}")
            sys.exit(1)

        self.stdout.write(f"Total rows processed: {row_num}")
        self.stdout.write(f"Data transfer time: --- {time.time() - start_time:.2f} seconds ---")
