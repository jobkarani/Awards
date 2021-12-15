from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Project, Profile
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import login, authenticate
from .serializer import *
from rest_framework.views import APIView
from .permissions import IsAdminOrReadOnly
from award import serializer
from rest_framework.response import Response

# Create your views here.


def home(request):
    images = Project.objects.all().order_by('-id')

    return render(request, 'all-temps/index.html', {'images': images})


@login_required(login_url='/accounts/login/')
def search_project(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search').lower()
        images = Project.search_project_name(search_term)
        message = f'{search_term}'

        return render(request, 'search.html', {'found': message, 'images': images})
    else:
        message = 'Not found'
        return render(request, 'all-temps/search.html', {'danger': message})


@login_required(login_url="/accounts/login/")
def create_profile(request):
    current_user = request.user
    title = "Create Profile"
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return HttpResponseRedirect('/')

    else:
        form = ProfileForm()
    return render(request, 'all-temps/create_profile.html', {"form": form, "title": title})


@login_required(login_url="/accounts/login/")
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    project = Project.objects.filter(user_id=current_user.id).all()

    return render(request, "all-temps/profile.html", {"profile": profile, "project": project})


@login_required(login_url="/accounts/login/")
def update_profile(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    form = UpdateProfileForm(instance=profile)
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():

            profile = form.save(commit=False)
            profile.save()
            return redirect('profile')

    ctx = {"form": form}
    return render(request, 'all-temps/update_prof.html', ctx)


@login_required(login_url="/accounts/login/")
def upload(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
        return redirect('/')
    else:
        form = ProjectForm()
    return render(request, 'all-temps/upload.html', {'form': form})


@login_required(login_url='/accounts/login/')
def rate(request, id):
    if request.method == 'POST':
        project = Project.objects.get(id=id)
        current_user = request.user
        design_value = request.POST['design']
        content_value = request.POST['content']
        usability_value = request.POST['usability']

        Rating.objects.create(
            project=project,
            user=current_user,
            design_value=design_value,
            usability_value=usability_value,
            content_value=content_value,
            average_value=round((float(design_value)+float(usability_value)+float(content_value))/3, 2),)

        return render(request, "all-temps/project.html", {"project": project})
    else:
        project = Project.objects.get(id=id)
        return render(request, "all-temps/project.html", {"project": project})


@login_required(login_url='/accounts/login/')
def project(request, project_id):
    project = Project.objects.get(id=project_id)
    rating = Rating.objects.filter(project=project)
    return render(request, "all-temps/project.html", {"project": project, "rating": rating})


class ProjectList(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
