from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import StudentProfile, InstituteProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # do not create both profiles by default; create on demand or detect group
        # Create both empty; alternative: use registration views to create correct profile
        StudentProfile.objects.create(user=instance)
        InstituteProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save related profiles if they exist
    try:
        instance.student_profile.save()
    except:
        pass
    try:
        instance.institute_profile.save()
    except:
        pass
