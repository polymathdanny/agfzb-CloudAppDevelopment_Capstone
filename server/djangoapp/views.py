from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from .models import CarMake, CarModel

from .restapis import *
from zlib import DEF_BUF_SIZE
from cloudant.client import Cloudant
from cloudant.error import CloudantException

from .forms import *
from .decorators import *
# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_request` view to handle sign in request
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index') # note: may need to change this back to 'home' at some point
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('djangoapp:index')
            else: 
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'djangoapp/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('djangoapp:login')

# Create a `registration_request` view to handle sign up request
def registrationPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)

            return redirect('djangoapp:login')

    context = {'form':form}
    return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = 'https://djangoapp1.us-south.cf.appdomain.cloud/api/dealerships/'

        # Get dealers from the URL
        dealerships = get_dealers_from_dict(url)

        states = get_dealerships_by_states_from_dict(url)
        #print(states)
        # Add relevant dealer info to list of dealer values

        dealers = {}
        for dealer in range(0, len(dealerships)):
            dealers[dealer] = {
                'dealer_id': dealerships[dealer].dealer_id,
                'name': dealerships[dealer].full_name,
                'address': dealerships[dealer].address,
                'city': dealerships[dealer].city,
                'state': dealerships[dealer].st
            }
        dealers = list(dealers.values())

        context = {'dealers': dealers, 'states':states}

        return render(request, 'djangoapp/index.html', context)
        #return HttpResponse(dealerships)




        
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships_by_id(request, pk, val):
    if request.method == "GET":
        url = 'https://djangoapp1.us-south.cf.appdomain.cloud/api/dealerships/' + pk +'/' + val + '/'
        print(url)
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

def get_dealerships_by_state(request, val):
    if request.method == "GET":
        url = 'https://djangoapp1.us-south.cf.appdomain.cloud/api/dealerships/state/' + val + '/'
        # Get dealers from the URL
        dealerships = get_dealers_from_dict(url)
        states = get_dealerships_by_states_from_dict(url)
        #print(states)
        # Add relevant dealer info to list of dealer values
        dealers = {}
        for dealer in range(0, len(dealerships)):
            dealers[dealer] = {
                'dealer_id': dealerships[dealer].dealer_id,
                'name': dealerships[dealer].full_name,
                'address': dealerships[dealer].address,
                'city': dealerships[dealer].city,
                'state': dealerships[dealer].st
            }
        dealers = list(dealers.values())
        print('******DEALERS*******')
        print(dealers)
        context = {'dealers': dealers, 'states': states}

        return render(request, 'djangoapp/index.html', context)

def aboutPage(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def contactPage(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

# Create a `registration_request` view to handle sign up request
# Create a `registration_request` view to handle sign up request
def add_review(request):
    if request.method == 'POST':
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            myDict = {
                "COUCH_URL": "https://98ff71f8-4e54-4bcc-bfbd-e91475399743-bluemix.cloudant.com/",
                "IAM_API_KEY": "WFGtu2LO6Ng7oLDafSfQNv0bYGvbVbJ76Y6jwguVeE39",
                "COUCH_USERNAME": "98ff71f8-4e54-4bcc-bfbd-e91475399743-bluemix"
            }

            client = Cloudant.iam(
                        account_name=myDict["COUCH_USERNAME"],
                        api_key=myDict["IAM_API_KEY"],
                        connect=True,
            )

            dbName = 'reviews'
            db = client[dbName]

            # Get number of documents in reviews db. The next id will be incremented
            i=0
            for doc in db:
                i = i+1
            id = i+1

            # Get dealership id from url params
            dealer_id = request.GET.get('dealership')

            # Initialize new document for POST request
            doc = {}
            doc['id'] = id
            doc['dealership'] = int(dealer_id)
            doc['name'] = form['name'].data
            doc['review'] = form['review'].data
            doc['purchase'] = form['purchase'].data

            # create doc in cloudant db
            db.create_document(doc, throw_on_exists=False)
            messages.success(request, 'success!')
            return redirect('djangoapp:index')
        else:
            # Failed attempt to create review. Alert user and send to contact site.
            messages.error(request, 'Failure!')
            return redirect('djangoapp:contact')
    else:
        car_makes = CarMake.objects.all()
        car_models = CarModel.objects.all()

        review_id = str(request.GET.get('dealership'))
        print(review_id)
        url = 'https://djangoapp1.us-south.cf.appdomain.cloud/api/reviews/dealership/' + review_id 
        print(url)
        reviews = get_reviews_from_dict(url)
        form = CreateReviewForm()
        context = {'form':form, 'reviews':reviews, 'car_makes': car_makes, 'car_model': car_models}
        return render(request, 'djangoapp/add_review.html', context)

