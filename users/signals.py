from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
    else:
        profile = Profile.objects.get(user=instance)
    profile.first_name = instance.first_name
    profile.last_name = instance.last_name
    profile.email = instance.email
    profile.save()

@receiver(pre_save, sender=Profile)
def delete_before_change(sender, instance, **kwargs):
    try: 
        profile = Profile.objects.get(pk = instance.pk)
    except Profile.DoesNotExist:
        profile = None

    if profile:
        old_pic = profile.profile_pic
        new_pic = instance.profile_pic.url
        
        if old_pic.url != new_pic and old_pic.url != "/media/avatar.png":
            old_pic.delete(save=False)

@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    if not created:
        user = User.objects.filter(profile=instance)
        user.update(
            first_name = instance.first_name,
            last_name = instance.last_name,
            email = instance.email
        )

    