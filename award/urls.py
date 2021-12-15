from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/<int:id>', views.update_profile, name='update_profile'),
    path('upload/project/', views.upload, name="upload"),
    path('accounts/profile/', views.home, name='profile'),
    path('project/<int:project_id>', views.project, name='project'),
    path('search/', views.search_project, name='search_project'),
    path('rate/<int:id>', views.rate, name='rate'),
    path('api/projects/', views.ProjectList.as_view()),
    path('api/profiles/', views.ProfileList.as_view()),
]
