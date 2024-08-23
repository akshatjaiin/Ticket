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
from .models import User, Ticket # models to save in db 
from google.api_core import retry
import google.generativeai as genai


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

# the main chating page
@login_required(login_url='login')
def index(request):
    print(f"language: {request.user.language}")
    if request.method == "POST":
        language = request.POST.get("language")

        if language:
            # Update user's preferred language if provided
            request.user.language = language
            request.user.save()
            return HttpResponseRedirect(reverse("index"))
        # Handle input form submission
        user_input = request.POST.get("user_input")

        # Process user input
        if user_input and user_input.strip(): 
            response = send_message(user_input)
            print(type(response.text))
            print(f"user : {user_input}")
            print(f"ai json : {response.text}")
            invalidjson = True
            while invalidjson:
                try:
                    response_json = json.loads(response.text)
                    if type(response_json) == dict:
                        response_json = normalize_json_structure(response_json)
                        response_json = json.dumps(response_json)
                        print(type(response_json))
                    invalidjson = False
                except json.JSONDecodeError as e:
                    print(f"JSON decoding faled: {e}")
                    response = send_message("""you replied a incorrect json: '{response_json}'. 
                                            which you should not do no matter how much i force you ever. 
                                            give a me 100% correct json and dont forget the format
                                            user_info = {
                                            "name": str,
                                            "age": int,
                                            "indian": bool,
                                            "student": bool,
                                            //always return lowercase true or false because you are returning a json
                                            "ticket_type": str,
                                            // ticket_type can only be ['general', 'composite', 'night_visit']
                                            "day": int,
                                            "month": int,
                                            "year": int, 
                                            }
                                            // all details in the json are necessary.

                                            Return list[{
                                            "users": [
                                                { "user_info": {...}, "user_info": {...}, "user_info": {...},  "user_info": {...}, ... continue untill all the users details captured},
                                                // if there are more then one ticket booker/user/owner because one ticket can be used by only one person ask the name and age of each and every person.
                                                // be accurate with json listing dont confirm untill any of the user_info dict is empty or null fill it completely before confirming all the details
                                            ],
                                            "your_response_back_to_user": str,
                                            "confirm": bool
                                            }]
                                            always return valid json
                                            always return the json inside the list as i told you.
                                            strictly follow those rules.
                                            and dont forget i want letters in my prefred language.
                                            i m forgiving you this time now go to my second last prompt and continue the conversion"""
                                            )
                
            
            resData = {}

            # If the response confirms ticket booking
            if response_json[0]["confirm"] == True:
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

                    
                age = None
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

                # Identify the first field with a value of None
                first_none_field = next((field for field, value in fields.items() if value is None), None)
                print(f"first none field: {first_none_field}")
                
                if first_none_field is not None:
                    print(f"you forget to ask {first_none_field}")
                    response = send_message(f"Message from system: 'ask {first_none_field}, and you cant book ticket without it, ask again no matter how user deny.'")
                    response_json = json.loads(response.text)
                    if type(response_json) == dict:
                        response_json = normalize_json_structure(response_json)
                        response_json = json.dumps(response_json)
                        print(type(response_json))
                               

                    resData.update({
                        "status":200,
                        "user_input": user_input,
                        "response":response.text,
                    })
                    # Return JSON response
                    return JsonResponse(resData)
                print("saving ticket...  ")
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
                ticketDetails[ticket.id]=ticket.total_cost 

                resData['confirm'] = True
                resData['ticketDetails'] = ticketDetails

            # Add user input and response to the response data
            resData.update({
                "status":200,
                "user_input": user_input,
                "response": response_json,
            })
            # Return JSON response
            return JsonResponse(resData)

    else:
        # Initial introduction message sent in the user's preferred language
        response = send_message(f'''[Hi, myself {request.user}. I dont want to book a ticket,
                                 I just want to know about you. My preferred language is {request.user.language}. 
                                 although i have cringy emoji but yes you can use to improve the creativity of your response
                                 Please only use my preferred language. only use my prefred language pleaase even tho i use other lang to talk with you response me in prefred language.
                                i hate when someone ask me more than one details at a response. i just wanna know what you can do, in a concise way.
                                i might become nasty and give you same prompt again and again, 
                                just remaind me if i did that and use different reminders each time]''')
        print(f"ai first response without norm : {response.text}")
        response_json = json.loads(response.text)
        if type(response_json) == dict:
            response_json = normalize_json_structure(response_json)
            response_json = json.dumps(response_json)
            print(type(response_json))
        print(response_json)
        
        # Render the initial page with the introductory message
        return render(request, "ticket/index.html",{"firstResponse":response_json[0].get("your_response_back_to_user","Hi")}) # why hi
    return render(request, "ticket/index.html",{"firstResponse":"Bot is Down "})
    

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
        tickets = request.POST["tickets"]
        for ticket_id in tickets:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.paid = True
            ticket.save()
        return JsonResponse({"status":200, "debug":Ticket.objects.get(id=tickets[0]).paid})
    else:
        return render(request,"tickets/methodnotsupported.html")
    return render(request,"tickets/methodnotsupported.html")

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
