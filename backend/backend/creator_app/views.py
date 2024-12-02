from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from cryptomus import Client
from .forms import PassengerForm, PassengerRegForm, AdminPassengerRegForm, ChildrenRegForm, ChildCardForm, AdultsRegForm, AdultsCardForm, CombineForm
from .models import Passenger, Passenger_Reg, Admin_Passenger_Reg, Children_form, ChildCard_form, Adults_form, AdultsCard_form, CombinedData
import pyrebase
import uuid
import logging
import json

# Logging configuration
logger = logging.getLogger(__name__)
CRYPTO_API_KEY = "4b6b1a51-796d-491e-8835-8c45b5a2afd1"
MERCHANT_UUID = '621379c1-acca-4252-bd66-2e86bfcff04'
PAYMENT_KEY = '1P9521ebLUosz8zANZEOlFTNreI6DkI8qKefuQaDWGzug8r3Wz7k3N2CEdIzj5OjgiaqUfVxismOqPND'

payment_client = Client.payment(PAYMENT_KEY, MERCHANT_UUID)

config = {
    "apiKey": "AIzaSyDB0fpsVB3K54VG56VNY1oNaGvCopY-yuc",
    "authDomain": "nfcdetails.firebaseapp.com",
    "databaseURL": "https://nfcdetails-default-rtdb.firebaseio.com",
    "projectId": "nfcdetails",
    "storageBucket": "nfcdetails.firebasestorage.app",
    "messagingSenderId": "1024977911201",
    "appId": "1:1024977911201:web:266a0f80919b3b07325fe0",
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

# Generic form handler
def handle_form(request, model, form_class, template_name, instance_id=0, redirect_url=None):
    if request.method == 'GET':
        if instance_id == 0:
            form = form_class()
        else:
            instance = get_object_or_404(model, pk=instance_id)
            form = form_class(instance=instance)
        return render(request, template_name, {"form": form})
    else:
        if instance_id == 0:
            form = form_class(request.POST)
        else:
            instance = get_object_or_404(model, pk=instance_id)
            form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            if redirect_url:
                return redirect(redirect_url)
        return render(request, template_name, {"form": form})



def passenger_form(request, id=0):
    return handle_form(
        request, Passenger, PassengerForm, 'creator_app/passenger_form.html', instance_id=id,
        redirect_url='creator_app:passenger_list'
    )


def passenger_list(request):
    passengers = Passenger.objects.all()
    return render(request, 'creator_app/passenger_list.html', {'passenger_list': passengers})


def passenger_delete(request, id):
    passenger = get_object_or_404(Passenger, pk=id)
    passenger.delete()
    return redirect('creator_app:passenger_list')


def combined_form(request, id=0):
    return handle_form(
        request, CombinedData, CombineForm, 'creator_app/combined_reg.html', instance_id=id,
        redirect_url='creator_app:combined_list'
    )


def combined_list(request):
    passengers1 = CombinedData.objects.all()
    return render(request, 'creator_app/combined_list.html', {'combined_list': passengers1})


def combined_delete(request, id):
    passenger1 = get_object_or_404(CombinedData, pk=id)
    passenger1.delete()
    return redirect('creator_app:combined_list')


def admin_passenger_form(request, id=0):
    return handle_form(
        request, Admin_Passenger_Reg, AdminPassengerRegForm, 'creator_app/admin_add_passenger.html',
        instance_id=id, redirect_url='creator_app:admin_passenger_list'
    )


def admin_passenger_list(request):
    passengers2 = Admin_Passenger_Reg.objects.all()
    return render(request, 'creator_app/admin_passenger_list.html', {'admin_passenger_list': passengers2})


def admin_passenger_delete(request, id):
    passenger2 = get_object_or_404(Admin_Passenger_Reg, pk=id)
    passenger2.delete()
    return redirect('creator_app:admin_passenger_list')

def passenger_home(request):
    return render(request, 'creator_app/passenger_home.html') 

def select_cat(request):
    return render(request, 'creator_app/select_cat.html')


ROUTE_PRICES = {
    ('Kaduwela', 'Kothalawala'): 50,
    ('Kothalawala', 'Malabe'): 40,
    ('Malabe', 'Thalangama'): 30,
    ('Thalangama', 'Koswatta'): 60,
    ('Koswatta', 'Battaramulla'): 70,
    ('Battaramulla', 'Welikada'): 80,
    ('Welikada', 'Rajagiriya'): 90,
    ('Rajagiriya', 'Ayurveda Junction'): 100,
    ('Ayurveda Junction', 'Castle Street'): 120,
    ('Castle Street', 'Devi Balika Junction'): 140,
    ('Devi Balika Junction', 'Senanayake Junction (Borella)'): 160,
    ('Senanayake Junction (Borella)', 'Horton Place'): 180,
    ('Horton Place', 'Liberty Junction'): 200,
    ('Liberty Junction', 'Kollupitiya (Station Road)'): 220,
}

def children_form(request, id=0):
    if request.method == "POST":
        if id == 0:
            form = ChildrenRegForm(request.POST)
        else:
            child = get_object_or_404(Children_form, pk=id)
            form = ChildrenRegForm(request.POST, instance=child)
        
        if form.is_valid():
            child = form.save(commit=False)

            route = (child.c_from, child.c_to)
            child.price = ROUTE_PRICES.get(route, 0)  
           
            child.save()
            return redirect('creator_app:children_list')
    else:
        if id == 0:
            form = ChildrenRegForm()
        else:
            child = get_object_or_404(Children_form, pk=id)
            form = ChildrenRegForm(instance=child)

    return render(request, 'creator_app/children_form.html', {'form': form})


def children_list(request):
    children = Children_form.objects.all()
    return render(request, 'creator_app/children_list.html', {'children_list': children})


def children_delete(request, id):
    child = get_object_or_404(Children_form, pk=id)
    child.delete()
    return redirect('creator_app:children_list')



def childrenCard_form(request, id=0):
    return handle_form(
        request, ChildCard_form, ChildCardForm, 'creator_app/childCard_form.html', instance_id=id,
        redirect_url='creator_app:childCard_list'
    )

def childrCard_list(request):
    childCards = ChildCard_form.objects.all()
    return render(request, 'creator_app/childCard_list.html', {'childCard_list': childCards})



def childrenCard_delete(request, id):
    childCard = get_object_or_404(ChildCard_form, pk=id)
    childCard.delete()
    return redirect('creator_app:childCard_list')



def adults_form(request, id=0):
    if request.method == "POST":
        if id == 0:
            form = AdultsRegForm(request.POST)
        else:
            adult = get_object_or_404(Adults_form, pk=id)
            form = AdultsRegForm(request.POST, instance=adult)
        
        if form.is_valid():
            # Save the form instance
            adult = form.save(commit=False)

            # Calculate ticket price
            route = (adult.a_from, adult.a_to)
            adult.price = ROUTE_PRICES.get(route, 0)  # Assign price or default to 0

            # Save the object to the database
            adult.save()
            return redirect('creator_app:adults_list')
    else:
        if id == 0:
            form = AdultsRegForm()
        else:
            adult = get_object_or_404(Adults_form, pk=id)
            form = AdultsRegForm(instance=adult)

    return render(request, 'creator_app/adults_form.html', {'form': form})


def adults_list(request):
    adults = Adults_form.objects.all()
    return render(request, 'creator_app/adults_list.html', {'adults_list': adults})


def adults_delete(request, id):
    adult = get_object_or_404(Adults_form, pk=id)
    adult.delete()
    return redirect('creator_app:adults_list')


def adultsCard_form(request, id=0):
    return handle_form(
        request, AdultsCard_form, AdultsCardForm, 'creator_app/adultsCard_form.html', instance_id=id,
        redirect_url='creator_app:adultsCard_list'
    )

def adultsCard_list(request):
    adultsCards = AdultsCard_form.objects.all()
    return render(request, 'creator_app/adultsCard_list.html', {'adultsCard_list': adultsCards})


def adultsCard_delete(request, id):
    adultCard = get_object_or_404(AdultsCard_form, pk=id)
    adultCard.delete()
    return redirect('creator_app:adultsCard_list')


##########################################

from coinbase_commerce.client import Client
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)

def create_payment(request):
    try:
        client = Client(api_key=settings.CRYPTO_API_KEY)
        charge_data = {
            "name": "Test Payment",
            "description": "Test description",
            "local_price": {"amount": "10.00", "currency": "USD"},
            "pricing_type": "fixed_price",
        }
        charge = client.charge.create(**charge_data)
        return render(request, 'payment.html', {'charge': charge})
    except Exception as e:
        logger.error(f"Error in create_payment: {e}")
        return JsonResponse({'error': 'Failed to create payment'}, status=500)

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event = data.get("event")
            logger.info(f"Received webhook event: {event}")
            # Add logic to handle the webhook event
            return JsonResponse({"status": "success"})
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return JsonResponse({"status": "error"}, status=400)
    return JsonResponse({"status": "failed"}, status=405)


def get_combined_data():
    # Query children forms
    children_forms = Children_form.objects.all()
    child_cards = ChildCard_form.objects.all()

    # Query adults forms
    adults_forms = Adults_form.objects.all()
    adults_cards = AdultsCard_form.objects.all()

    # Combine the data into a unified list
    combined_data = []

    # Process Children data
    for child_form in children_forms:
        combined_data.append({
            'type': 'child',
            'to': child_form.c_to,
            'from': child_form.c_from,
            'price': child_form.price,
            'name': None,
            'address': None,
            'mobile': None,
        })
    for child_card in child_cards:
        combined_data.append({
            'type': 'child',
            'to': None,
            'from': None,
            'price': None,
            'name': child_card.childName,
            'address': child_card.childAddress,
            'mobile': child_card.childMobile,
        })

    # Process Adults data
    for adult_form in adults_forms:
        combined_data.append({
            'type': 'adult',
            'to': adult_form.a_to,
            'from': adult_form.a_from,
            'price': adult_form.price,
            'name': None,
            'address': None,
            'mobile': None,
        })
    for adult_card in adults_cards:
        combined_data.append({
            'type': 'adult',
            'to': None,
            'from': None,
            'price': None,
            'name': adult_card.adultsName,
            'address': adult_card.adultsAddress,
            'mobile': adult_card.adultsMobile,
        })

    return combined_data


def combined_data_view(request):
    combined_data = get_combined_data()
    return render(request, 'creator_app/combined_table.html', {'combined_data': combined_data})

def admin_home(request):
    return render(request, 'creator_app/admin_home.html')

def manage_passengers(request):
    return render(request, 'creator_app/manage_passengers.html')

def combined_table(request):
    return render(request, 'creator_app/combined_table.html')