from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_otp_group(sender, **kwargs):
    if sender.name == 'app':
        group, created = Group.objects.get_or_create(name='OTP')
        if created:
            print("Group 'OTP' created successfully.")
        else:
            print("Group 'OTP' already exists.")
