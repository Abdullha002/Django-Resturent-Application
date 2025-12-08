from . models import User, UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver


# receiver

# We can use this decorator -> @receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

    else:
        # delete the userprofile get error
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create the userprofile if not exist
            UserProfile.objects.create(user=instance)

# Or this line to connect the signal
post_save.connect(post_save_create_profile_receiver, sender=User)