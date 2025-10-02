from django.contrib import admin
from .models import Course, InstituteProfile, OfferedCourse, StudentProfile

admin.site.register(Course)
admin.site.register(InstituteProfile)
admin.site.register(OfferedCourse)
admin.site.register(StudentProfile)
