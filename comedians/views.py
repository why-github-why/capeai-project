from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from requests.models import HTTPError
from .models import Comedian
import requests
import random

def register(request):
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      confirm_password = request.POST['confirm_password']

      # check if passwords match
      if password == confirm_password:

         # check if username exists
         if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already in use.')
            return redirect('register')
         else:
            # create user
            user = User.objects.create_user(
               username = username,
               password = password,
            )
            user.save()

            messages.success(request, 'You\'re registered.')
            return redirect('login')

      else:
         messages.error(request, 'Passwords doesn\'t match.')
         return redirect('register')

   else:
      return render(request, 'comedians/register.html')


def login(request):
   if request.method == 'POST':
      # acquire login credentials
      username = request.POST['username']
      password = request.POST['password']

      # authenticate user
      user = auth.authenticate(username=username, password=password)

      # check if user is registered
      if user is not None:
         auth.login(request, user)
         messages.success(request, 'You\'re logged in.')
         return redirect('index')
      else:
         messages.error(request, 'Invalid credentials.')
         return redirect('login')

   else:
      return render(request, 'comedians/login.html')


def logout(request):
   if request.method == 'POST':
      # logout comedian (user)
      auth.logout(request)
      messages.success(request, 'You\'re logged out.')
      return redirect('index')


def about(request):
   if request.method == "POST":
      username = request.POST['username']
      inspiration = request.POST['inspiration']
      joke_of_the_day = request.POST['joke_of_the_day']

      # create comedian
      comedian = Comedian(
         username = username,
         inspiration = inspiration,
         joke_of_the_day = joke_of_the_day,
         )
      comedian.save()

      context = {
         'inspiration': inspiration,
         'joke_of_the_day': joke_of_the_day,
      }

      return render(request, 'comedians/about.html', context)


def more(request):
   try:
      url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"

      params = {
         "format":"json",
         "blacklistFlags":"nsfw,racist"
      }

      headers = {
         'x-rapidapi-key': "609d5f5caemsh5c0473a6335e3afp1d5eeejsn4370056b4ff7",
         'x-rapidapi-host': "jokeapi-v2.p.rapidapi.com"
      }

      response = requests.request("GET", url, headers=headers, params=params)
      joke = response.json()

      try:
         joke_setup = joke["setup"]
         joke_delivery = joke["delivery"]

      except KeyError as k:
         print(k)

         joke_setup = "No more jokes,"
         joke_delivery = "Please try again later."
      

   except HTTPError as e:
      print(e)

      context = {
         'joke_setup': "Why are there gates around cemeteries?",
         'joke_delivery': "Because people are dying to get in!",
      }

   else:
      context = {
         'joke_setup': joke_setup,
         'joke_delivery': joke_delivery,
      }

      return render(request, 'comedians/more.html', context)