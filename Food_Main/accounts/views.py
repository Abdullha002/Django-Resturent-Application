from django.shortcuts import render, redirect
from . forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages, auth

# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are logged in")
        return redirect('dashboard')
    
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
        # create the user using form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = user.CUSTOMER
            # user.save()

        #    OR   This

        # create the user  using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = user.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registred successfully")

            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        'form' : form,
    }
    return render(request, "accounts/registerUser.html", context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are logged in")
        return redirect('dashboard')
    
    if request.method =="POST":
        # Store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = user.RESTUARENT
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user = user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your account has been registred successfully! Please wait for the approval.")

            return redirect('registerVendor')

    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form'  : form,
        'v_form' : v_form
    }
    return render(request, "accounts/registerVendor.html", context)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are logged in")
        return redirect('dashboard')
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')

    return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    messages.info(request, "You are loged out")
    return redirect('login')


def dashboard(request):
    user = request.user
    user.get_role_display()
    if user.role == 1:
        user.role = "Restuarent"
    else:
        user.role = "Customer"

    context = {
        'user' : user
    }
    return render(request, "accounts/dashboard.html", context)


def customerDashboard(request):
    return render(request, "accounts/customerDash.html")

def vendorDashboard(request):
    pass