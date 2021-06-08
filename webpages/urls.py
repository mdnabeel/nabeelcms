from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('addfault', views.addfault, name="addfault"),
    path('search', views.search, name="search"),
    path('update', views.update, name="update"),
    path('edit/<int:pk>/', views.edit, name="edit"),
    path('export', views.export, name="export"),

]
