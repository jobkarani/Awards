from django.test import TestCase
from django.contrib.auth.models import User
from .models import Project, Profile

# Create your tests here.


class ProjectTestClass(TestCase):  # Project class test
    def setUp(self):
        # creating a user
        user = User.objects.create(
            username="ayub", first_name="ayub", last_name="254"
        )

        self.project = Project(
            name="art",
            about="about art",
            image="https://cdn.pixabay.com/photo/2016/03/31/20/27/avatar-1295773__340.png",
            user=user,
        )

    def test_instance(self):
        self.assertTrue(isinstance(self.project, Project))

    def test_save_method(self):
        self.project.save_project()
        projects = Project.objects.all()
        self.assertTrue(len(projects) > 0)


class ProfileTestClass(TestCase):
    def setUp(self):

        user = User.objects.create(
            username="ayub", first_name="ayub", last_name="254"
        )

        self.profile = Profile(
            bio="hey there",
            user=user,
            contact="09876",
        )

    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))

    def test_save_method(self):
        self.profile.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)
