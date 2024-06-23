from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AccountHolder


@receiver(post_save, sender=User)
def create_account_holder(sender, instance, created, **kwargs):
    if created:
        AccountHolder.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_account_holder(sender, instance, **kwargs):
    instance.accountholder.save()
