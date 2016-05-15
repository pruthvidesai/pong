# TODO: implement logging
import logging

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from pingpong.forms import UserForm, UserProfileForm


def index(request):
    # dictionary thats used in as a parameter
    context_dict = {'boldmessage' : "Hi! I'm bold!"}

    # Note the first parameter is the template we wish to use.
    return render(request, 'pingpong/index.html', context_dict)


def register(request):
    logging.info("Inside Register")
    # a boolean value for telling template whether the registration was successful
    registered = False

    # if it's HTTP POST we're interested in processing form data
    if request.method == 'POST':
        # attempt to grab information from raw form information
        # making use of both UserForm and UserProfileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # save user's form to database
            user = user_form.save()

            # hash user's password
            # once hashed, save user's object
            user.set_password(user.password)
            user.save()

            # now we sort out UserProfileForm
            # Since we create this attribute ourselves, we commit=False
            # delaying saving models to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # did user provide a profile picture?
            # if so, we need to get the input and put it in UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # now we save the UserProfle model instance
            profile.save()

            # time to update register variable
            registered = True

        # print errors on terminal if forms invalid
        # it'll also be shown to the user
        else:
            print user_form.errors, profile_form.errors

    # if not an HTTP POST, we render our two ModelForm instances
    # render would be empty, ready for input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # render the template based on the request
    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, 'pingpong/register.html', context_dict)

def user_login(request):

    # if the request is POST try to pull the relevant information
    if request.method == 'POST':
        # gather username and password provided by user
        # this information is obtained from login() form
            # we use request.POST.get('<variable>') instead of request.POST['<variable>']
            # because former will return None, if value doesn't exist, 
            # and latter will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the abscence of a value), no user
        # with matching credentials was found
        if user:
            # is the account active? could have been disabled
            if user.is_active:
                # If valid and active
                # we'll send the user back to homepage
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Your account is disabled')
        else:
            # bad login details provided, can't log in
            print "Invalid login credentials: %s, %s" % (username, password)
            return HttpResponse("Invalid login credentials")

    # method is not POST so display login form.
    else:
        # no context variables to pass
        # that's why empty dictionary
        context_dict = {}
        return render(request, 'pingpong/login.html', context_dict)

# this decorater ensures that we need user to be logged in
@login_required
def user_logout(request):
    # since we know user is logged in, we can log him out.
    logout(request)

    # redirecting to Homepage
    return HttpResponseRedirect('/')