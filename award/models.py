from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
import datetime as dt
from tinymce.models import HTMLField

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    profile_photo = CloudinaryField('image')
    bio = models.TextField(max_length=650, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.save()

    def update(self):
        self.save()

    def __str__(self):
        return self.user.username
