from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile
from . models import Vendor
from . forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from menu.models import Category, FoodItem

# Create your views here.

def profile(request):
    profile = get_object_or_404(UserProfile, user = request.user)
    vendor = get_object_or_404(Vendor)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Setting Updated!")
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form' : profile_form,
        'vendor_form' : vendor_form,
        'profile' : profile,
        'vendor' : vendor
    }
    return render(request, 'vendor/vend_profile.html', context)

def menu_builder(request):
    vendor = Vendor.objects.get(user = request.user)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories' : categories
    }
    return render(request, "vendor/menu_builder.html", context)

def fooditem_by_category(request, pk=None):
    vendor = Vendor.objects.get(user = request.user)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor,category=category)
    context = {
        'category' : category,
        'fooditems' : fooditems
    }
    return render(request, "vendor/fooditem_by_category.html", context)