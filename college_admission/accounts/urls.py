from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('register/student/', views.student_register, name='student_register'),
    path('register/institute/', views.institute_register, name='institute_register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("profile/", views.profile, name="profile"),

    path('student/complete-profile/', views.student_complete_profile, name='student_complete_profile'),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path('institute/complete-profile/', views.institute_complete_profile, name='institute_complete_profile'),
    path('institute/offered-courses/', views.institute_offered_courses, name='institute_offered_courses'),
    path('institute/offered-courses/create/', views.offered_course_create, name='offered_course_create'),
    path('institute/offered-courses/<int:pk>/edit/', views.offered_course_edit, name='offered_course_edit'),
    path('institute/offered-courses/<int:pk>/submit/', views.offered_course_submit, name='offered_course_submit'),

    path('student/institutes/', views.list_institutes_for_students, name='student_institutes'),
]
