import time
import sys
import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from organization.models import Ergasies, Organization , Employee # Adjust import paths for your app

import sys
import csv
import time
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Load Employees from CSV into the database"

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        start_time = time.time()
        path = kwargs['path']
        max_rows = 100  # Limit for testing

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

                total_rows = sum(1 for _ in reader)
                f.seek(0)  # Reset file pointer to the beginning
                next(reader, None)  # Skip the header row again

                for row_num, row in enumerate(reader, start=1):
                    # Stop processing if the row limit is reached
                    if row_num > max_rows:
                        self.stdout.write(f"Row limit of {max_rows} reached. Stopping import.")
                        break

                    row = [None if cell == 'NULL' else cell for cell in row]
                    try:
                        if len(row) < 4:  # Ensure there are enough columns
                            raise ValueError("Row does not contain the required number of columns.")

                        # Replace username with email if necessary
                        username = row[4]  # Assuming username is in the 5th column (index 4)
                        if username == "athanasia":
                            username = "akarakousi@acsservices.gr"
                        elif username == "kostasvit":
                            username = "kostasvit@gmail.com"
                        elif username == "kostas":
                            username = "kostasvit@gmail.com"
                        elif username == "alexis":
                            username = "amav@acsservices.gr"
                        elif username == "geo":
                            username = "gmav@acsservices.gr"
                        elif username == "eirini":
                            username = "etourgeli@acsservices.gr"
                        elif username == "gmpek":
                            username = "gmpek@acsservices.gr"
                        elif username == "amaz":
                            username = "amaz@acsservices.gr"
                        elif username == "panagiotis":
                            username = "ptselos@acsservices.gr"

                        # Get the custom User model
                        User = get_user_model()
                        employee = User.objects.filter(email=username).first() if username else None

                        if not employee:
                            raise ValueError(f"Employee with email {username} not found.")

                        # Query the Organization object
                        organization = Organization.objects.get(name=row[1]) if row[1] else None
                        org_employee = Employee.objects.get(lastname=row[7]) if row[7] else None
                        # Update or create Ergasies record
                        Ergasies.objects.update_or_create(
                            old_id=row[0],
                            organization=organization,
                            employee=employee,
                            org_employee=org_employee,
                            defaults={
                                'importdate': row[2],
                                'app': row[3],
                                'jobtype': row[4],
                                'info': row[5],
                                'text': row[6],
                                'time': row[8],
                                # Add any other fields you need to update here
                            }
                        )

                    except Exception as err:
                        with open('errors.csv', 'a', encoding='utf-8-sig') as error_file:
                            error_writer = csv.writer(error_file, delimiter=',', quotechar='"')
                            if row_num == 1:  # Write header only once
                                error_writer.writerow(['row_num', 'organization', 'importdate', 'app', 'jobtype', 'info', 'text', 'employee', 'time', 'org_employee', 'ticketid', 'error'])
                            error_writer.writerow([row_num] + row + [str(err)])
                        self.stderr.write(f"Invalid data in row {row_num}. Skipping...")
                        self.stderr.write(f"Row: {row}, Reason: {err}")

                    # Calculate and display progress percentage
                    progress = min(100, int((row_num / min(total_rows, max_rows)) * 100))
                    self.stdout.write(f"Progress: {progress}% complete", ending="\r")
                    self.stdout.flush()

        except FileNotFoundError:
            self.stderr.write(f"File not found: {path}")
            sys.exit(1)
        except Exception as e:
            self.stderr.write(f"An unexpected error occurred: {e}")
            sys.exit(1)

        self.stdout.write(f"\nTotal rows processed: {min(row_num, max_rows)}")
        self.stdout.write(f"Data transfer time: --- {time.time() - start_time:.2f} seconds ---")


