import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quality_analysis.settings')
django.setup()
import pandas as pd
from django.db import transaction
from analysis.models import YearGroup, Subject, Student, GradeMapping, Performance

GRADE_FILE = '/home/abdul/PycharmProjects/quality_analysis/data/Grades.xlsx'
MARKS_FILE = '/home/abdul/PycharmProjects/quality_analysis/data/Marks.xlsx'

# Default grade-to-numerical-value mapping
DEFAULT_GRADE_MAPPING = {
    "A*": 95,
    "A": 85,
    "B": 75,
    "C": 65,
    "D": 55,
    "E": 45,
    "F": 35,
    "G": 25,
    "9": 95,
    "8": 85,
    "7": 75,
    "6": 65,
    "5": 55,
    "4": 45,
    "3": 35,
    "2": 25,
    "1": 15,
    "U": 0,
    "WT": 45,
    "OT": 65,
    "EX": 90,
    "BE": 75,
}

def import_data():
    # Load Excel files
    marks_data = pd.ExcelFile(MARKS_FILE).parse('Sheet1')
    grades_data = pd.ExcelFile(GRADE_FILE).parse('Sheet1')

    with transaction.atomic():
        # Import Year Groups
        print("Processing Year Groups...")
        for year in marks_data['Year'].unique():
            year_group, created = YearGroup.objects.get_or_create(name=year)
            print(f"YearGroup: {year_group.name}, Created: {created}")

        # Import Subjects

        for subject_name in marks_data['Subject'].unique():
            subject, created = Subject.objects.get_or_create(name=subject_name)
            print(f"Subject: {subject.name}, Created: {created}")

        # Import Students and Marks
        print("Processing Marks File...")
        for _, row in marks_data.iterrows():
            try:
                # Get or create the student
                year_group = YearGroup.objects.get(name=row['Year'])
                student, created = Student.objects.get_or_create(
                    adno=row['Adno'],
                    defaults={
                        'first_name': row.get('Forename', 'Unknown'),
                        'last_name': row.get('Legal Surname', 'Unknown'),
                        'gender': row.get('Gender', 'Unknown'),
                        'current_year_group': year_group,
                    }
                )

                # Get or create the subject
                subject = Subject.objects.get(name=row['Subject'])

                # Create or update Performance
                performance, created = Performance.objects.get_or_create(
                    student=student,
                    subject=subject,
                    academic_year=row['Academic Year'],
                    defaults={'marks': row['Marks']}
                )
                if not created:
                    performance.marks = row['Marks']
                    performance.save()



            except Exception as e:
                print(f"Error processing row in Marks File: {row}, Error: {e}")

        # Import Grades
        print("Processing Grades File...")
        for _, row in grades_data.iterrows():
            try:
                # Get the student and subject
                student = Student.objects.get(adno=row['Adno'])
                subject = Subject.objects.get(name=row['Subject'])

                # Update Performance with grade
                performance = Performance.objects.filter(
                    student=student,
                    subject=subject,
                    academic_year=row['Academic Year']
                ).first()

                if performance:
                    performance.grade = row['Grade']
                    performance.save()

                else:
                    print(f"Performance record not found for Grade update: {row}")

                # Optionally, populate GradeMapping for later use
                if row['Grade'] not in DEFAULT_GRADE_MAPPING:
                    print(f"Skipping unrecognized grade: {row['Grade']}")
                    continue

                grade_mapping, _ = GradeMapping.objects.get_or_create(
                    academic_year=row['Academic Year'],
                    subject=subject,
                    grade=row['Grade'],
                    defaults={'numerical_value': DEFAULT_GRADE_MAPPING[row['Grade']]}
                )

            except Exception as e:
                print(f"Error processing row in Grades File: {row}, Error: {e}")

    print("Data import completed.")

# Run the script
if __name__ == '__main__':
    import_data()