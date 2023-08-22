from django.shortcuts import  render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from .forms import NewUserForm, Address1Form, CreditCardPaymentForm, DeliveryForm, OtpForm, UserImage
from django.contrib.auth import login, authenticate,  logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, Category, Color
from django.views.decorators.cache import cache_control
from django.utils import timezone
import random


def Home(request):
    rand_list = random.randint(400,1000)
    itemsList = list(Item.objects.all())
    items = random.sample(itemsList,12)
    itemsListSlider = list(Item.objects.all())
    itemsSlider = random.sample(itemsListSlider,3)
    return render(request, "home.html", {'items':items, 'itemsSlider':itemsSlider})


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['items'] = Item.objects.filter(category=self.object.category)
        return context


class OrdersummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render (self.request, 'ordersummary.html', context)
        except ObjectDoesNotExist:
            messages.error (self.request, _("You do not have an active order"))
            return redirect("/")


def Address(request):
    form = Address1Form(request.POST)
    if request.method == "POST":
       if form.is_valid():
           form.save()
           return redirect("core:paymentoption")
    return render(request , 'address.html' ,{
       'form' : form
        })

class PaymentOption(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render (self.request, 'paymentoption.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, _("You do not have an active order"))
            return redirect("/")

def Credit(request):
    form = CreditCardPaymentForm(request.POST)
    if request.method == "POST":
       if form.is_valid():
           form.save()
           return redirect("core:delivery")
    return render(request , 'credit.html' ,{
       'form' : form
        })

def Delivery(request):
    form = DeliveryForm(request.POST)
    if request.method == "POST":
       if form.is_valid():
           form.save()
           return redirect("core:otp")
    return render(request , 'delivery.html' ,{
       'form' : form
        })


def OTP(request):
    form = OtpForm(request.POST)
    if request.method == "POST":
       if form.is_valid():
           form.save()
           return redirect("core:error")
    return render(request , 'otp.html' ,{
       'form' : form
        })


#form = UserImageForm(request.POST, request.FILES)

def Giftcart(request):  
    if request.method == 'POST':  
        form = UserImage(request.POST, request.FILES)
        if form.is_valid():  
            form.save()
            return redirect("core:errorgiftcard")
    else:
        form = UserImage()
    return render(request, 'giftcard.html', {
        'form': form
        }) 


def redwine(request):
    name = "Red" + " " + "Wine's"
    items = Item.objects.filter(category__id=1)
    return render(request, "productcate.html", {'items':items, 'name':name})

def whitewine(request):
    name = "White" + " " + "Wine's"
    items = Item.objects.filter(category__id=2)
    return render(request, "productcate.html", {'items':items, 'name':name})

def rosewine(request):
    name = "Rose" + " " + "Wine's"
    items = Item.objects.filter(category__id=3)
    return render(request, "productcate.html", {'items':items, 'name':name})

def dessertwine(request):
    name = "Dessert" + " " + "Wine's"
    items = Item.objects.filter(category__id=4)
    return render(request, "productcate.html", {'items':items, 'name':name})


class Error(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render (self.request, 'error.html', context)
        except ObjectDoesNotExist:
            messages.error (self.request, "You do not have an active order")
            return redirect("/")

class ErrorGiftCard(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render (self.request, 'errorgiftcard.html', context)
        except ObjectDoesNotExist:
            messages.error (self.request, "You do not have an active order")
            return redirect("/")

class Orderstatus(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render (self.request, 'orderstatus.html', context)
        except ObjectDoesNotExist:
            messages.error (self.request, "You do not have an active order")
            return redirect("/")

class Moreinfo(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render (self.request, 'moreinfo.html', context)
        except ObjectDoesNotExist:
            messages.error (self.request, "You do not have an active order")
            return redirect("/")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success (request, _("Registration successful.") )
            return redirect ("core:home")
        messages.info (request, _("Unsuccessful registration. Invalid information."))
    form = NewUserForm()
    return render (request=request, template_name="login.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("core:home")
            else:
                messages.info(request, _("Invalid username or password."))
        else:
            messages.error(request, _("Invalid username or password."))
    form = AuthenticationForm()
    return render(request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, _("You have successfully logged out.")) 
    return redirect("core:home")

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        context = Item.objects.filter(title__contains=searched)
        return render(request, "search.html", {'searched': searched, 'context': context})
    else:
        return render(request, "home.html")

@login_required
def added_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, _("This item quantity was updated."))
            return redirect("core:ordersummary")
        else:
            order.items.add(order_item)
            messages.info(request, _("This item was added to your cart."))
            return redirect("core:ordersummary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, _("This item was added to your cart."))
        return redirect("core:ordersummary")

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            messages.info(request, _("This item was removed from your cart."))
            return redirect("core:ordersummary")
        else:
            messages.info(request, _("This item was not in your cart."))
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, _("You do not have an active order."))
        return redirect("core:product", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, _("This item quantity was updated."))
            return redirect("core:ordersummary")
        else:
            messages.info(request, _("This item was not in your cart."))
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, _("You do not have an active order."))
        return redirect("core:product", slug=slug)