from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User

import os
print (os.getcwd())

import csv
import json
from random import randint
from typing import Iterable
from dotenv import load_dotenv
from google.api_core import retry
import google.generativeai as genai

# cofiguring model api 
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel(
    "gemini-1.5-flash",
)

MUSEUM_BOT_PROMPT = open('bot_prompt.txt', 'r', encoding='utf-8').read()



# Select the model name based on the toggle
model_name = 'gemini-1.5-flash'
safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model = genai.GenerativeModel(model_name, generation_config= {'response_mime_type': "application/json"}, safety_settings=safe)
convo = model.start_chat(
    history=[
        {'role': 'user', 'parts': [MUSEUM_BOT_PROMPT]},
        {'role': 'model', 'parts': ['OK I will fill response back to user to continue chat with him.']}
    ],
    enable_automatic_function_calling=True
)

@retry.Retry(initial=30)
def send_message(message):
    """Send a message to the conversation and return the response."""
    return convo.send_message(message)


# Main loop for user interaction
while False:
    user_input = input('> ').strip()
    if user_input.lower() == "quit":
        break

        

    if user_input != "":
        response = send_message(user_input)
        
        response_json = json.loads(response.text)
        print(response_json[0]["your_response_back_to_user"])

        if response_json[0]["confirm"] == True:
            print("\n\n\n\n")
            for i in response_json[0]["users"]:
                print(i['user_info'])
            print("\n\nprocessing to payment gateway ........")
        
   
  
    




@login_required(login_url='login')
def index(request):
    return render(request, "ticket/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
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

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "ticket/register.html", {
                "message": "username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ticket/register.html")

