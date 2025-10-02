from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .forms import StudentRegisterForm, InstituteRegisterForm, StudentProfileForm, InstituteProfileForm, OfferedCourseForm
from .models import OfferedCourse, InstituteProfile, StudentProfile

# Student registration
def student_register(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            students_group, created = Group.objects.get_or_create(name="Students")
            user.groups.add(students_group)
            # create student profile (if not via signals)
            StudentProfile.objects.get_or_create(user=user)
            # log the user in
            login(request, user)
            return redirect("accounts:student/complete-profile/")
    else:
        form = StudentRegisterForm()
    return render(request, 'accounts:student_complete_profile', {'form': form})



@login_required
def student_dashboard(request):
    return render(request, "accounts/student_dashboard.html")

@login_required
def profile(request):
    return render(request, "accounts/profile.html")

# Institute registration
def institute_register(request):
    if request.method == "POST":
        form = InstituteRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="Institutes")
            user.groups.add(group)
            InstituteProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("/accounts/student/complete-profile/")
    else:
        form = InstituteRegisterForm()
    return render(request, 'accounts/institute_register.html', {'form': form})

@login_required
def student_complete_profile(request):
    # ensure user is in Students group
    if not request.user.groups.filter(name="Students").exists():
        return redirect('home')
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # if they applied to a offered_course, mark has_applied_before
            if profile.applied_offered_course:
                profile.has_applied_before = True
                profile.save()
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'accounts/student_complete_profile.html', {'form': form})

@login_required
def institute_complete_profile(request):
    if not request.user.groups.filter(name="Institutes").exists():
        return redirect('home')
    profile, _ = InstituteProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = InstituteProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('institute_offered_courses')
    else:
        form = InstituteProfileForm(instance=profile)
    return render(request, 'accounts/institute_complete_profile.html', {'form': form})

@login_required
def institute_offered_courses(request):
    profile = get_object_or_404(InstituteProfile, user=request.user)
    offered = profile.offered_courses.all()
    return render(request, 'accounts/institute_offered_courses.html', {'offered': offered})

@login_required
def offered_course_create(request):
    profile = get_object_or_404(InstituteProfile, user=request.user)
    if request.method == 'POST':
        form = OfferedCourseForm(request.POST, request.FILES)
        if form.is_valid():
            oc = form.save(commit=False)
            oc.institute = profile
            oc.save()
            return redirect('institute_offered_courses')
    else:
        form = OfferedCourseForm()
    return render(request, 'accounts/offered_course_form.html', {'form': form})

@login_required
def offered_course_edit(request, pk):
    oc = get_object_or_404(OfferedCourse, pk=pk, institute__user=request.user)
    if request.method == 'POST':
        form = OfferedCourseForm(request.POST, request.FILES, instance=oc)
        if form.is_valid():
            form.save()
            return redirect('institute_offered_courses')
    else:
        form = OfferedCourseForm(instance=oc)
    return render(request, 'accounts/offered_course_form.html', {'form': form, 'offered': oc})

@login_required
def offered_course_submit(request, pk):
    oc = get_object_or_404(OfferedCourse, pk=pk, institute__user=request.user)
    oc.is_submitted = True
    oc.save()
    return redirect('institute_offered_courses')

# Student view: list institutes that have submitted offerings
@login_required
def list_institutes_for_students(request):
    # Show institutes that have at least one submitted OfferedCourse
    offered = OfferedCourse.objects.filter(is_submitted=True).select_related('institute','course')
    # group by institute
    institutes = {}
    for oc in offered:
        institutes.setdefault(oc.institute, []).append(oc)
    return render(request, 'accounts/student_institute_list.html', {'institutes': institutes})
