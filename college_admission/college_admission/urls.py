from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.student_register, name="student_register"),
    path('accounts/', include('accounts.urls')),
]