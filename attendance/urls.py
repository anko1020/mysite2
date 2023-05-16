from django.urls import path

from . import views

urlpatterns = [
    path('', views.Login, name='Login'),
    #path("logout", views.Logout, name="Logout"),
    path("result", views.Result, name="Result"),
    path("adminform", views.AdminFrom.as_view(), name="AdminForm"),
    path("edit/<int:pk>/", views.AccountEditer, name="Edit"),
    path("register", views.Registration.as_view(), name="Register"),
    path("pdf/<int:pk>", views.DownloadExcel ,name="PopExcel"),
    path("daily", views.daily ,name="Daily"),
    path("seat", views.SelectSeat.as_view(), name="SelectSeat"),
    path("checksheet/<int:pk>", views.CheckEditer.as_view(), name="CheckSheet"),
    path("compSheet/<int:pk>", views.CompCheckSheet.as_view(), name="CompSheet"),
    path("control", views.control, name="Control"),
]