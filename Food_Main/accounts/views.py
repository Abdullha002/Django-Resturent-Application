from django.shortcuts import render, redirect
from . forms import UserForm
from vendor.forms import VendorForm
from vendor.models import Vendor
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email, send_reset_password_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Restricting the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restricting the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are logged in")
        return redirect('myAccount')
    
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

            # send verification email
            send_verification_email(request, user)

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
        return redirect('myAccount')
    
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

            # send verification email
            send_verification_email(request, user)

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
        return redirect('myAccount')
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in")
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')

    return render(request, "accounts/login.html")


def logout(request):
    auth.logout(request)
    messages.info(request, "You are loged out")
    return redirect('login')


# def dashboard(request):
#     user = request.user
#     user.get_role_display()
#     if user.role == 1:
#         user.role = "Restuarent"
#     else:
#         user.role = "Customer"

#     context = {
#         'user' : user
#     }
#     return render(request, "accounts/dashboard.html", context)


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, "accounts/customerDash.html")

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.grt(user = request.user)
    context = {
        'vendor' : vendor,
    }
    return render(request, "accounts/vendorDash.html", context)

# activate registration process
def activate(request, uidb64, token):
    # Activating the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token) :
        user.is_active = True
        user.save()
        messages.success(request, "Congratulation your account is activated")
        return redirect('myAccount')
    else:
        messages.error(request, "Invalid activation Link")
        return redirect('myAccount')
    


def forgot_password(request):
    if request.method == 'POST':
        email_id = request.POST['email']
        if User.objects.filter(email = email_id).exists():
            user = User.objects.get(email__exact = email_id)


            # send reset password email
            send_reset_password_email(request, user)
    return render(request, "accounts/emails/forgot_password.html")


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token) :
        request.session['uid'] = uid
        messages.info(request, "Please reset your password")
        return redirect('reset_password')
    else:
        messages.error(request, "This link has been expired")
        return redirect('myAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password reset Successfull")
            return redirect('login')
        else:
            messages.error(request, "Password do not match")
            return redirect('reset_password')
    return render(request, "accounts/emails/reset_password.html")