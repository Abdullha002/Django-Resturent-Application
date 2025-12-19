from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile
from . models import Vendor
from . forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from menu.models import Category, FoodItem
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from django.core.exceptions import PermissionDenied
from menu.forms import CategoryForm, FooditemForm
from django.template.defaultfilters import slugify

# Create your views here.

# Helper function
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

# Profile function

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
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

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories' : categories
    }
    return render(request, "vendor/menu_builder.html", context)

# Category functionalities

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditem_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor,category=category)
    context = {
        'category' : category,
        'fooditems' : fooditems
    }
    return render(request, "vendor/fooditem_by_category.html", context)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "Category added successfully!")
            return redirect('menu_builder')
        
    else:
        form = CategoryForm()
    context = {
        'form':form,
    }
    return render(request, "vendor/add_category.html", context)

def edit_category(request, cat_id=None):
    category = get_object_or_404( Category, id=cat_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, "Category updated successfully!")
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category' : category
    }
    return render(request, "vendor/edit_category.html", context)

def delete_category(request, cat_id=None):
    category = get_object_or_404( Category, id=cat_id)
    category.delete()
    messages.success(request, "Category has been deleted successfully!")
    return redirect('menu_builder')

# Food items functionalities

def add_food(request):
    if request.method == 'POST':
        form = FooditemForm(request.POST, request.FILES)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            food.save()
            messages.success(request, "Food Item added successfully!")
            return redirect('fooditem_by_category', food.category.id)

    else:        
        form = FooditemForm()
    context = {
        'form' : form
    }
    return render(request, "vendor/add_food.html", context)

def edit_food(request, food_id):
    food_item = get_object_or_404( FoodItem, id=food_id)
    if request.method == 'POST':
        form = FooditemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            foodtitle = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(foodtitle)
            food.save()
            messages.success(request, "Food Item updated successfully!")
            return redirect('fooditem_by_category', food.category.id)
    else:
        form = FooditemForm(instance=food_item)
    context = {
        'form':form,
        'food_item' : food_item
    }
    return render(request, "vendor/edit_food.html", context)

def delete_food(request, food_id):
    food = get_object_or_404( FoodItem, id=food_id)
    food.delete()
    messages.success(request, "Food item has been successfully deleted!")
    return redirect('fooditem_by_category', food.category.id)