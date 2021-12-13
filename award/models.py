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


class Project(models.Model):
    name = models.CharField(max_length=50)
    cat = models.TextField(max_length=20)
    location = models.TextField(max_length=20)
    image = CloudinaryField('image')
    url = models.URLField(max_length=60, null=True)
    about = models.TextField(max_length=2000)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def _str_(self):
        return self.name

    @classmethod
    def get_all_projects(cls):
        projects = Project.objects.all()
        return projects

    @classmethod
    def search_by_name(cls, search_term):
        projects = cls.objects.filter(name__icontains=search_term)
        return projects

    @classmethod
    def display_all_projects(cls):
        return cls.objects.all()

    def save_project(self):
        self.save()

    def update_project(self, name, description, category):
        self.name = name,
        self.description = description,
        self.category = category
        self.save()

    class Meta:
        ordering = ['-created_on']
