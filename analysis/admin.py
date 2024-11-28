from django.contrib import admin
from .models import YearGroup, Subject, Student, GradeMapping, Performance

admin.site.register(YearGroup)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(GradeMapping)
admin.site.register(Performance)
