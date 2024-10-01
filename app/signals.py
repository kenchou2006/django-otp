from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings

@receiver(post_migrate)
def create_otp_group(sender, **kwargs):
    if sender.name == 'app':
        group, created = Group.objects.get_or_create(name='OTP')
        if created:
            print("Group 'OTP' created successfully.")
        else:
            print("Group 'OTP' already exists.")

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username=settings.DEFAULT_SUPERUSER_USERNAME,
            email=settings.DEFAULT_SUPERUSER_EMAIL,
            password=settings.DEFAULT_SUPERUSER_PASSWORD
        )
        print("Superuser 'admin' created successfully.")