from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import Pastry, Blogs, Order, OrderItem, Billing
from tracker.models import OrderUpdate
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from .forms import CheckoutForm
from django.utils import timezone
from django.contrib.auth.models import User
import json
from django.http import HttpResponse
# Create your views here.
def index(request):
    
    pastry = Pastry.objects.all()
    blogs = Blogs.objects.all()
    return render(request, 'index.html', {'pastry': pastry , 'blogs': blogs})

# def checkout(request):
#     pastry = Pastry.object.all()
#     return render(request, 'checkout.html', {'pastry' : pastry})

# class HomeView(ListView):
#     model = Pastry, Blogs
#     template_name = 'index.html'
class CheckOutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'checkout.html', context)
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_Address = form.cleaned_data.get('apartment_Address')
                country = form.cleaned_data.get('country')
                zips = form.cleaned_data.get('zips')
                same_address = form.cleaned_data.get('same_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing = Billing(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_Address = apartment_Address,
                    country = country,
                    zips = zips
                )
                billing.save()
                order.billing = billing
                order.save()
                update = OrderUpdate(Order_id=order.id, Update_desc="The order has been placed successfully!", user=order.user)
                update.save()
                if payment_option == 'G':
                    messages.success(self.request, "You order id is "+str(order.id)+"You can track it with this id")
                    return redirect("pastryHome:payment", payment_option='google_pay')
                elif payment_option == 'P':
                    messages.success(self.request, "You order id is "+str(order.id)+"You can track it with this id")
                    return redirect("pastryHome:payment", payment_option='paytm')
                elif payment_option == 'C':
                    messages.success(self.request, "You order id is "+str(order.id)+"You can track it with this id")
                    # messages.success(self.request, "Your order has been submitted successfully")
                    return redirect("/")
                else:
                    messages.warning(self.request,"Invaild payment option")
                    return redirect("pastryHome:checkout")

        except ObjectDoesNotExist:
            messages.error(self.request, "you have no order!")
            return redirect("pastryHome:order-summary")

class Payment(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, 'payment.html', context)



@login_required
def add_to_cart(request, slug):
    if request.user.is_authenticated:
        item = get_object_or_404(Pastry, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user = request.user,
            ordered = False
        )
        order_qs = Order.objects.filter(user = request.user, ordered = False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug = item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "Quantity was updated!")
                return redirect ("pastryHome:order-summary")
            else:
                order.items.add(order_item)
                messages.info(request, "Item Added")
                return redirect ("pastryHome:order-summary")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user = request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request, "Item Added")
            return redirect("pastryHome:order-summary")
    else:
        messages.info(request, "Please login to continue!")
        return render(request, "index.html")
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Pastry, slug=slug)
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():#order checking
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "Item Removed")
            return redirect ("pastryHome:order-summary")
        else:
            messages.info(request, "Item is not in the cart")
            return redirect ("pastryHome:index")#a message for user of no order
    else:
        messages.info(request, "You have no order")
        return redirect ("pastryHome:index")#a message for user of no order

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            context = {
                'object' : order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "you have no order!")
            return redirect("/")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Pastry, slug=slug)
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():#order checking
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity>0:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "Item quantity updated")
            return redirect ("pastryHome:order-summary")
        else:
            messages.info(request, "Item is not in the cart")
            return redirect ("pastryHome:order-summary")#a message for user of no order
    else:
        messages.info(request, "You have no order")
        return redirect ("pastryHome:order-summary")#a message for user of no order


# def TrackView(request):
#     if request.method == "POST":
#         order_id = request.POST.get('order_id', '')
#         user = request.POST.get('user', '')
#         try:
#             order = OrderUpdate.objects.filter(order_id = order_id, user=user)
#             print(order)
#             # order_id = order.order_id
#             if len(order) > 0:
#                 update = OrderUpdate.objects.filter(order_id=order_id)
#                 updated = []
#                 for item in update:
#                     updated.append({'text':item.update_desc, 'time':item.timestamp})
#                     response = json.dumps(updated)
#                     return HttpResponce(response)
#             else:
#                 messages.error(request, "You have no order of this ID")
#                 return redirect("pastryHome:track")
#         except ObjectDoesNotExist:
#             messages.error(self.request, "You have no order of this ID")
#             return redirect("pastryHome:track")
#     return render(request, 'track.html')