# django modules
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
# models to save in db 
from .models import User, Ticket
# some needed modules
import os
import json
from dotenv import load_dotenv
# modeules to load ai 
from google.api_core import retry
import google.generativeai as genai
# some constants which we are using
from . import constants;

# cofiguring model api 
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Select the model name based on the toggle
model_name = 'gemini-1.5-flash'
# Toggle this to switch between Gemini 1.5 with a system instruction, or Gemini 1.0 Pro.
use_sys_inst = False

# Initialize the model with safety settings
if use_sys_inst:
    model = genai.GenerativeModel(
        model_name, system_instruction=constants.MUSEUM_BOT_PROMPT, safety_settings=constants.SAFE, 
        generation_config= {'response_mime_type': "application/json"}
    )
    convo = model.start_chat(enable_automatic_function_calling=True)
else:
    model = genai.GenerativeModel(model_name, generation_config= {'response_mime_type': "application/json"}, safety_settings=constants.SAFE)
    convo = model.start_chat(
        history=[
            {'role': 'user', 'parts': [constants.MUSEUM_BOT_PROMPT]},
            {'role': 'model', 'parts': ['OK I will fill response back to user to continue chat with him.']}
        ],
        enable_automatic_function_calling=True
    )

# a func to chat with ai :)
@retry.Retry(initial=30)
def send_message(message)->None:
    """Send a message to the conversation and return the response."""
    return convo.send_message(message)

# the main chating page
@login_required(login_url='login')
def index(request):
    if request.method == "POST":
        print(request.POST);

        # Handle form submission
        user_input = request.POST.get("user_input")
        language = request.POST.get("language")

        # Update user's preferred language if provided
        if language:
            request.user.language = language
            request.user.save()

        # Process user input
        if user_input and user_input.strip(): 
            response = send_message(user_input);
            response_json = json.loads(response.text);
            resData = {}

            # If the response confirms ticket booking
            if response_json[0]["confirm"] == True:
                ticketDetails = {};
                for user_data in response_json[0]["users"]:
                    name = user_data['user_info']['name']
                    age = user_data['user_info']['age']
                    indian = user_data['user_info']['indian']
                    student = user_data['user_info']['student']
                    ticket_type = user_data['user_info']['ticket_type']
                    day = user_data['user_info']['day']
                    month = user_data['user_info']['month']
                    year = user_data['user_info']['year']
                    book_date = date(year, month, day)
                    paid = False

                    # Create and save the ticket
                    ticket = Ticket(
                        name=name,
                        age=age,
                        indian=indian,
                        student=student,
                        ticket_type=ticket_type,
                        date=book_date,
                        owner=request.user,
                        paid=paid
                    )
                    ticket.save()
                    # this is to send the user the price of the ticket acd to there id 
                    ticketDetails[ticket.id]=ticket.total_cost; 

                resData['confirm'] = True
                resData['ticketDetails'] = ticketDetails;

            # Add user input and response to the response data
            resData.update({
                "user_input": user_input,
                "response": response.text,
            })
            # Return JSON response
            return JsonResponse(resData)

    elif request.method == "GET":
        # Initial introduction message sent in the user's preferred language
        response = send_message(f"Hi, myself {request.user}. I may or may not want to book a ticket, but I want to know about you. My preferred language is {request.user.language}. Please use my preferred language and give an energetic intro. only use my prefred language pleaase")
        response_json = json.loads(response.text)
        # Render the initial page with the introductory message
        return render(request, "ticket/index.html")
    else:
        return "Method Not Supported";

# creating a ticket url for every ticket so that user can acess those;
@login_required(login_url='login')
def ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    year = ticket.date.year
    month = ticket.date.month
    day = ticket.date.day

    return render(request, "ticket/ticket.html", {
        "name": ticket.name,
        "age": ticket.age,
        "indian": ticket.indian,
        "student": ticket.student,
        "ticket_id": ticket.id,
        "day": day,
        "month": month,
        "year": year,
        "ticket_type": ticket.ticket_type,
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if not user:
            login(request, user) # login the user
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ticket/login.html", {
                "message": "Invalid username and/or password."
            })

    elif request.method == "GET":
        return render(request, "ticket/login.html")
    else:
        # for other request like DELET or PUT etc 
        return "Method Not Supported";


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
        # make user login
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        return render(request, "ticket/register.html")
    else:
        # for other request like DELET or PUT etc 
        return "Method Not Supported";


def about_museum(request):
    if request.method == "GET":
        return render(request, "ticket/about_museum.html")
    else:
        # for other request like DELET or PUT etc 
        return "Method Not Supported";

