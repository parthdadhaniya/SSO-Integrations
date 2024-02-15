from django.http import HttpResponse
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.


def login(request):
    return render(request, "login.html")


def azuread_login(request):
    auth_url = f"{settings.AZURE_AD_AUTH_URL}?client_id={settings.AZURE_AD_CLIENT_ID}&response_type=code&redirect_uri={settings.REDIRECT_URI}"
    return redirect(auth_url)


def azuread_callback(request):
    code = request.GET.get("code")
    token_data = {
        "grant_type": "authorization_code",
        "client_id": settings.AZURE_AD_CLIENT_ID,
        "code": code,
        "redirect_uri": settings.REDIRECT_URI,
        "client_secret": settings.AZURE_AD_CLIENT_SECRET,
        "resource": "https://graph.microsoft.com",
    }
    response = requests.post(settings.AZURE_AD_TOKEN_URL, data=token_data)
    token_response = response.json()
    access_token = token_response.get("access_token")
    user_info_url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_info_url, headers=headers)
    user_data = user_response.json()
    email = user_data.get("mail")
    if email:
        try:
            user = User.objects.get(email=email)

            if user is not None:
                login(request, user)
                success_message = _(f"Successfully signed in as {user.username}.")
                messages.success(request, success_message)
                return render(request, "dashboard.html")
            else:
                return HttpResponse("Authentication failed.")
        except Exception as e:
            return HttpResponse(f"{e}")
