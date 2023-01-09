from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from django.contrib.auth import login, logout, authenticate
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger

logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return render(request, 'djangoapp/index.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/6a703ea1-bc6a-438e-9a62-cf094e484ee1/default/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/6a703ea1-bc6a-438e-9a62-cf094e484ee1/default/get-reviews"
    reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
    reviews = ' '.join([review.review + " " + review.sentiment for review in reviews])
    return HttpResponse(reviews)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if not request.user.is_authenticated:
        return HttpResponse("Not logged in, could not add review")

    if request.method == "POST":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/6a703ea1-bc6a-438e-9a62-cf094e484ee1/default/post-reviews"
        review = {
            "dealership": dealer_id,
            "name": "Kenny",
            "purchase": "Honda Civic",
            "review": "This is a great car dealer",
            "purchase_date": datetime.utcnow().isoformat(),
            "car_make": "sedan",
            "car_model": "Honda",
            "car_year": 2006,
        }
        json_payload = {
            "review": review
        }
        result = post_request(url, json_payload, dealerId=dealer_id)
        return HttpResponse(result)

    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html')
