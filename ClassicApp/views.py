import json

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests.auth import HTTPBasicAuth

from ClassicApp.credentials import MpesaAccessToken, LipanaMpesaPpassword
from ClassicApp.models import Contact, Member, Product, Cart


# Create your views here.
def home(request):
    if request.method == 'POST':
        if Member.objects.filter(
            username = request.POST['username'],
            password = request.POST['password']
        ).exists():
            return render(request, 'home.html')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
def about(request):
    return render(request, 'about.html')
def collection(request):
    return render(request, 'collection.html')

def contacts(request):
    if request.method == 'POST':
        clients = Contact(
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            message = request.POST['message']
        )
        clients.save()
        return redirect( '/contact')
    else:
        return render(request, 'contact.html')


def base(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        members = Member(
            name = request.POST['name'],
            username = request.POST['username'],
            password = request.POST['password'],
        )
        members.save()
        return redirect('login')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        if Member.objects.filter(
                username=request.POST['username'],
                password=request.POST['password']
        ).exists():
            return render(request, 'home.html')
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def categories(request):
    products = Product.objects.all()
    return render(request, 'categories.html', {'products': products})

def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = product.related_products.all()  # Fetch related products
    return render(request, 'details.html', {
        'product': product,
        'related_products': related_products,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')


def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        stripe.PaymentIntent.create(
            amount=int(total_price * 100),  # Amount in cents
            currency="ksh",
            payment_method_types=["card"],
        )
        # Clear cart after successful payment
        cart_items.delete()
        return redirect('success')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})



def token(request):
    consumer_key = 'GBBuxTDooeeNglVRxJZUUF5XPDz9wny80Bf6hpFF20A6GVm2'
    consumer_secret = 'zgayLTqQHAKlH9J3qtyYRKhzjguBGtIsVixqM57RZ8KPLvQUgHgofaVSTJUAKTk7'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
   return render(request, 'pay.html')



def stk(request, ):
    cart_items = Cart.objects.filter(user=request.user)
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "ClassicThrift",
            "TransactionDesc": "purchases Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        cart_items.delete()
        return redirect('success')
    return render(request, 'checkout.html', {'cart_items': cart_items, })

def success(request):
    return render(request, 'success.html')