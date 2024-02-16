from django.urls import path
from app.views import azuread_callback, azuread_login, login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", login, name="login"),
    path("azuread/login/", azuread_login, name="azuread_login"),
    path("oauth-authorized/azure/", azuread_callback, name="azuread_callback"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
