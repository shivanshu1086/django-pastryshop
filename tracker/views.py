from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from pastryHome.models import Pastry, Blogs, Order, OrderItem, Billing
from .models import OrderUpdate
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from pastryHome.forms import CheckoutForm
from django.utils import timezone
from django.contrib.auth.models import User
import json
from django.http import HttpResponse

# Create your views here.
def TrackView(request):
    if request.method == "POST":
        Order_id = request.POST.get('Order_id', '')
        user = request.POST.get('user', '')
        try:
            if User.objects.get(email=user):
                print("Email Verified")
                if OrderUpdate.objects.filter(Order_id=Order_id).exists():
                    print("Order id verified")
                    update = OrderUpdate.objects.filter(Order_id=Order_id)
                    updates = []
                    for items in update:
                        updates.append({'text':items.Update_desc, 'time':items.timestamp})
                        response = json.dumps(updates, default=str, ensure_ascii=False)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{}')
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'track.html')