from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


def user_login(request):
    if request.user.is_authenticated == True:
        return redirect("home_app:home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data.get("username"))
            login(request, user)
            return redirect("home_app:home")
    else:
        form = LoginForm()
    return render(request, template_name="account/login.html", context={"form": form})


def user_register(request):
    context = {"errors": []}
    if request.user.is_authenticated == True:
        return redirect("home_app:home")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            context['errors'].append("passwords dose not in same")
            return render(request, template_name="account/register.html", context=context)

        # if User.objects.get(username=username):
        #     context['errors'].append("this username is exists")
        #     return render(request, template_name="account/register.html", context=context)
        user = User.objects.create(username=username, password=password1, email=email)
        login(request, user)
        return redirect("home_app:home")
    return render(request, template_name="account/register.html", context={})

def user_edit(request):
    pass
def user_logout(request):
    logout(request)
    return redirect("home_app:home")
