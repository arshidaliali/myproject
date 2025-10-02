from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile, InstituteProfile, OfferedCourse

class StudentRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    class Meta:
        model = User
        fields = ('username','password1','password2','email')  # email optional

class InstituteRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    class Meta:
        model = User
        fields = ('username','password1','password2','email')

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['photo','full_name','father_name','cnic_number','applied_offered_course']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # limit offered courses to those submitted by institutes
        self.fields['applied_offered_course'].queryset = OfferedCourse.objects.filter(is_submitted=True)

class InstituteProfileForm(forms.ModelForm):
    class Meta:
        model = InstituteProfile
        fields = ['name','contact_email','address']

class OfferedCourseForm(forms.ModelForm):
    class Meta:
        model = OfferedCourse
        fields = ['course','teacher_name','teacher_cv','classroom_images','equipment_list']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # If creating new offered course, course list is standard Course objects
