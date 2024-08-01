from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import EmailDataForm, UserLoginForm, UserRegistrationForm
from .models import Mail


# Create your views here.
def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse("profile"))
    else:
        form = UserRegistrationForm()

    context = {"title": "Регистрация", "form": form}
    return render(request, "users/registration.html", context=context)


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("profile"))
    else:
        form = UserLoginForm()

    context = {"title": "Авторизация", "form": form}
    return render(request, "users/login.html", context=context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse("login"))


@login_required
def profile(request):
    if request.method == "POST":
        form = EmailDataForm(data=request.POST)
        if form.is_valid():
            email_login = request.POST["email_login"]
            email_password = request.POST["email_password"]
            user = request.user
            Mail.objects.get_or_create(
                user=user, email=email_login, password=email_password
            )
            return HttpResponseRedirect(reverse("mail"))
    else:
        form = EmailDataForm()
    return render(request, "users/profile.html")


@login_required
def mail(request):
    return render(request, "mails/mails.html")
