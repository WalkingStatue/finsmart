from django.db.models.signals import post_save
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.dispatch import receiver
from django.db import models

# Create your models here.
class Account(models.Model):
    user=models.OneToOneField('auth.User',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_pics',blank=True,null=True)
    profile_completed = models.BooleanField(default=False)
    on_delete=models.CASCADE
    related_name='account'

    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User)
def create_user_account(sender,instance,created,**kwargs):
    if created:
        Account.objects.create(user=instance)