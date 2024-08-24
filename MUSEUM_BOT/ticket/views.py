# django modules
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.sessions.models import Session
from django.shortcuts import  render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse  

# import
import os
import json
from . import constants # some constants which we are using
from datetime import date
from dotenv import load_dotenv
# Import date class from datetime module
from datetime import date
from .models import User, Ticket # models to save in db 
from google.api_core import retry
import google.generativeai as genai

def get_date():
    # return current date
    return date.today() 

load_dotenv() # load env
genai.configure(api_key=os.getenv('GEMINI_API_KEY')) # cofiguring model api 

model_name = 'gemini-1.5-flash'

# Initialize the model with safety settings
model = genai.GenerativeModel(
    model_name, system_instruction=constants.MUSEUM_BOT_PROMPT, safety_settings=constants.SAFE, 
    generation_config= {'response_mime_type': "application/json"}
)
convo = model.start_chat(history=[
        {'role': 'user', 'parts': [constants.MUSEUM_BOT_PROMPT]},
        {'role': 'model', 'parts': ['OK I will fill response back to user to continue chat with him.']}
    ], enable_automatic_function_calling=True)

def makeValidJson(jsonData)->list:
    if isinstance(jsonData, dict):
        print("Dict Detected, handling...")
        return [jsonData];
    return jsonData;
    
def strToJSON(jsonStr: str)->list|dict:
    try:
        return json.loads(jsonStr)
    except json.JSONDecodeError as err:
        print("ai sended a destructured response");
        return strToJSON(send_message(f"Incorrect JSON response: '{response.text}'. Please follow the correct format."));

def normalize_json_structure(data):
    # If the input is a string, try to load it as JSON
    if isinstance(data, str):
        try:
            parsed_data = json.loads(data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    else:
        # If data is already a list or dictionary, use it as-is
        parsed_data = data
    # Unwrap nested single-item lists
    while isinstance(parsed_data, list) and len(parsed_data) == 1:
        parsed_data = parsed_data[0]

    # If the final structure is a dictionary, wrap it in a list
    if isinstance(parsed_data, dict):
        return [parsed_data]

    # If the final structure is a list of dictionaries, return as-is
    if isinstance(parsed_data, list) and all(isinstance(item, dict) for item in parsed_data):
        return parsed_data

    # If it doesn't match any known structure, raise an error
    raise ValueError("Unknown JSON structure")

# a func to chat with ai :)
@retry.Retry(initial=30)
def send_message(message)->None:
    """Send a message to the conversation and return the response."""
    return convo.send_message(message)

@login_required(login_url='login')
def index(request):
    if request.method == "POST":
        # changing user lang
        if(language := request.POST.get("language")):
            # Update user's preferred language if provided
            request.user.language = language
            request.user.save()
            return HttpResponseRedirect(reverse("index"))

        # Handle input form submission
        user_input = request.POST.get("user_input",False)
        if not user_input:
            print(user_input)
            return JsonResponse({"status":400,"message":"Bad request","successful":False});
        elif not user_input.strip():
            return JsonResponse({"status":400,"message":"Bad request","successful":False});

        response = send_message(user_input)
        # for debuging we are gonna remove it at last
        print(f"user : {user_input}")
        print(f"ai json : {response.text}")

        # Parse the AI response and ensure valid JSON
        response_json = strToJSON(response.text);
        response_json = makeValidJson(response_json);

        resData = {}
        # Check if the response confirms ticket booking
        if response_json[0]["confirm"]:
            ticketDetails = {}
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

                # Validate that all required fields are provided
                fields = {
                    'name': name,
                    'age': age,
                    'indian': indian,
                    'student': student,
                    'ticket_type': ticket_type,
                    'day': day,
                    'month': month,
                    'year': year
                }

                first_none_field = next((field for field, value in fields.items() if value is None), None)
                if first_none_field:
                    print(f"Missing field: {first_none_field}")
                    response = send_message(f"Message from system: 'Please ask for {first_none_field}. You cannot book a ticket without it.'")
                    response_json = strToJSON(response.text);
                    response_json = makeValidJson(response_json);
                    resData.update({
                        "status": 200,
                        "user_input": user_input,
                        "response": response.text,
                    })
                    return JsonResponse(resData)
                
                # Save the ticket
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

                # Calculate the ticket price
                ticketDetails[ticket.id] = ticket.total_cost

            resData['confirm'] = True
            resData['ticketDetails'] = ticketDetails

        # Add user input and AI response to the response data
        resData.update({
            "status": 200,
            "user_input": user_input,
            "response": response_json,
            "successful":True,
            "message":"ai response fetched successful",
        })
        return JsonResponse(resData)
    elif request.method == "GET":
        # Send an initial introduction message in the user's preferred language
        response = send_message(f"""[Hi, myself {request.user}. I don't want to book a ticket,
                                    I just want to know about you. My preferred language is {request.user.language}. 
                                    Although I have cringy emojis, you can use them to improve the creativity of your response.
                                    Please only use my preferred language, even if I use another language to talk with you.
                                    I hate when someone asks me more than one detail in a response. 
                                    I just want to know what you can do in a concise way.
                                    I might repeat the same prompt again and again, 
                                    just remind me if I do that and use different reminders each time.]""")
        print(f"AI first response: {response.text}")
        response_json = makeValidJson(strToJSON(response.text));
        return render(request, "ticket/index.html", {"firstResponse": response_json[0].get("your_response_back_to_user", "Hi")})
    else: 
        return JsonResponse({"message":"Method not allowed","status":405}) 
    

# creating a ticket url for every ticket so that user can acess those
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


@login_required(login_url='login')
def makepaymentsuccess(request):
    if request.method == "POST":
        tickets = json.loads(request.body.decode('utf-8'));
        print("ticket conf , tickets:",tickets,type(tickets));
        for ticket_id in tickets["tickets"]:
            ticket = Ticket.objects.get(id=int(ticket_id))
            ticket.paid = True # mark the tickets paid if payment is successful
            ticket.save()
        return JsonResponse({"status": 200, "successful": Ticket.objects.get(id=tickets["tickets"][0]).paid})
    return JsonResponse({"message":"Method not allowed","status":405}) 

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user) # login the user
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ticket/login.html", {
                "message": "Invalid username and/or password."
            })

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
        # make user login
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "ticket/register.html")

def about_museum(request):
    return render(request, "ticket/about_museum.html")


def booked(request):
     return render(request, "ticket/booked.html", 
                   {
                       "tickets": Ticket.objects.all().filter(paid=True, owner=request.user)
                   })

