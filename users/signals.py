from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core. mail import send_mail
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            user_name=user.username,
            email=user.email,
            name=user.first_name,
        )
        
        subject = "Welcome To Devsearch"
        content = "Welcome to website from owner to you 'Ahmed Heikal' enjoy"

        send_mail(
            subject,
            content,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )




@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    pass


@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    try:
      user = instance.user
      user.delete()
    except:
        pass  

