from django.urls import path

from . import views

urlpatterns = [
    path('', views.Login, name='Login'),
    #path("logout", views.Logout, name="Logout"),
    path("result", views.Result, name="Result"),
    path("adminform", views.AdminFrom.as_view(), name="AdminForm"),
    path("edit/<int:pk>/", views.AccountEditer, name="Edit"),
    path("register", views.Registration.as_view(), name="Register"),
    path("pdf/<slug:user>", views.PDF ,name="PopPDF"),
    path("daily", views.daily ,name="Daily"),
    path("control", views.control, name="Control"),
]