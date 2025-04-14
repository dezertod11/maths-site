"""proj_maths URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('problems-list/', views.problems_list, name='problems-list'),
    path('add-problem/', views.add_problem, name='add-problem'),
    path('send-problem/', views.send_problem, name='send-problem'),
    path('solve-problem/', views.solve_problem, name='solve-problem'),
    path('check-solution/', views.check_solution, name='check-solution'),
    path('stats/', views.show_stats, name='stats'),
]