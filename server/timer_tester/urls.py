from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hit_miss', views.hit_miss, name='hit_miss'),
    path('distribution', views.distribution, name = 'distribution'),
    path('rdtsc', views.rdtsc, name='rdtsc'),
]
