from django.db import models

class YearGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)  # E.g., Year 8, Year 9

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)  # E.g., Science, Biology

    def __str__(self):
        return self.name


class Student(models.Model):
    adno = models.IntegerField(unique=True)  # Admission number
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    current_year_group = models.ForeignKey(YearGroup, on_delete=models.SET_NULL, null=True, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.adno})"


class GradeMapping(models.Model):
    academic_year = models.CharField(max_length=9)  # E.g., 2023-2024
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grade_mappings')
    grade = models.CharField(max_length=10)  # E.g., A*, A, B
    numerical_value = models.FloatField(null=True, blank=True)  # Normalized score for comparisons

    def __str__(self):
        return f"{self.academic_year} - {self.subject.name} - {self.grade} ({self.numerical_value})"


class Performance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='performances')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='performances')
    academic_year = models.CharField(max_length=9)  # E.g., 2023-2024
    grade = models.CharField(max_length=10, null=True, blank=True)  # Directly store grade for now
    marks = models.FloatField(null=True, blank=True)  # Numeric marks

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.academic_year})"
