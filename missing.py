import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quality_analysis.settings')
django.setup()
from analysis.models import Subject
import pandas as pd

# Load the Marks and Grades files
GRADE_FILE = '/home/abdul/PycharmProjects/quality_analysis/data/Grades.xlsx'
MARKS_FILE = '/home/abdul/PycharmProjects/quality_analysis/data/Marks.xlsx'

# Load the Marks and Grades files
marks_data = pd.read_excel(MARKS_FILE)
grades_data = pd.read_excel(GRADE_FILE)

# Extract unique subjects
unique_marks_subjects = set(marks_data['Subject'].unique())
unique_grades_subjects = set(grades_data['Subject'].unique())

# Compare subjects between the two files
missing_in_grades = unique_marks_subjects - unique_grades_subjects
missing_in_marks = unique_grades_subjects - unique_marks_subjects

# Print results
if missing_in_grades:
    print("Subjects found in Marks file but missing in Grades file:")
    for subject in missing_in_grades:
        print(f" - {subject}")
else:
    print("No unique subjects in Marks file compared to Grades file.")

if missing_in_marks:
    print("\nSubjects found in Grades file but missing in Marks file:")
    for subject in missing_in_marks:
        print(f" - {subject}")
else:
    print("\nNo unique subjects in Grades file compared to Marks file.")