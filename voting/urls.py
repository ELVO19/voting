from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('vote/', views.vote_view, name='vote'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
    path('results/', views.results_view, name='results'),
]