from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Owner


def index(request):
    return render(request, "ticket/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign Owner in
        username = request.POST["username"]
        password = request.POST["password"]
        Owner = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if Owner is not None:
            login(request, Owner)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ticket/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "ticket/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "ticket/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new Owner
        try:
            Owner = Owner.objects.create_Owner(username, email, password)
            Owner.save()
        except IntegrityError:
            return render(request, "ticket/register.html", {
                "message": "username already taken."
            })
        login(request, Owner)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ticket/register.html")
