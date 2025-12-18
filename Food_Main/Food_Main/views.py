from django.shortcuts import render, redirect
from vendor.models import Vendor

def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    context = {
        'vendors' : vendors
    }
    return render(request, "home.html", context)