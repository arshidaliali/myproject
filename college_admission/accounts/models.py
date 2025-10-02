from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class InstituteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="institute_profile")
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    # courses offered via OfferedCourse
    def __str__(self): return f"{self.name} ({self.user.username})"

class OfferedCourse(models.Model):
    institute = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, related_name="offered_courses")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=200, blank=True)
    teacher_cv = models.FileField(upload_to="teacher_cvs/", blank=True, null=True)
    classroom_images = models.ImageField(upload_to="classrooms/", blank=True, null=True)
    equipment_list = models.TextField(blank=True)  # or JSONField if structured
    is_submitted = models.BooleanField(default=False)  # institute final submission
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('institute', 'course')

    def __str__(self): return f"{self.institute.name} — {self.course.name}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    photo = models.ImageField(upload_to="student_photos/", blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True)
    father_name = models.CharField(max_length=200, blank=True)
    # Student chooses a specific offered course (institute + course)
    applied_offered_course = models.ForeignKey(OfferedCourse, on_delete=models.SET_NULL, null=True, blank=True, related_name='applicants')
    cnic_number = models.CharField(max_length=15, blank=True)  # validate formatting if needed
    has_applied_before = models.BooleanField(default=False)    # or use StudentApplication model

    def __str__(self):
        return f"{self.user.username} profile"
