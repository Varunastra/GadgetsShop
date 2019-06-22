from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, render
import json
import pickle
from os import path
from django.views.generic import View
from catalog.models import ShopItem
import logging
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import Order, Discount, CustomUser, ProfitUser
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import datetime
import numpy as np
from django.apps import apps
from .models import Cart
logger = logging.getLogger("mylogger")

# Create your views here.


def transform_json(cart_list):
    response = []
    for key in cart_list:
        item = list(ShopItem.objects.filter(id=key).values())
        item.append(cart_list[key])
        response.append(item)
    return json.dumps(list(response), cls=DjangoJSONEncoder)


def add_to_cart(request):
    data = json.loads(request.body)
    pk = data['id']
    quantity = data['quantity']
    session_cart = request.session.get("cart_list")
    cart_list = {}
    if session_cart is not None:
        cart_list = session_cart
    cart_list[str(pk)] = quantity
    request.session['cart_list'] = cart_list
    return HttpResponse("")


def get_cart(request):
    session_cart = request.session.get("cart_list")
    if session_cart is None:
        session_cart = {}
    return HttpResponse(transform_json(session_cart), content_type="application/json")


def remove_from_cart(request):
    data = json.loads(request.body)
    id = data['id']
    session_cart = request.session.get("cart_list")
    session_cart.pop(id)
    request.session["cart_list"] = session_cart
    return HttpResponse("")


def clear_session(request):
    request.session.flush()
    return HttpResponse("")


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    template_name = 'cart/checkout.html'

    def get(self, request):
        if request.session.get('cart_list') == {}:
            return HttpResponseRedirect(reverse('items_view'))
        return render(request, self.template_name)


def getPredictionData(price, quantity, gender, age, category):
    if gender == 'Male':
        gender = 0
    else:
        gender = 1
    categories = ['Cables', 'Covers', 'Headphones', 'Phones', 'SDCards', 'Tablets']
    one_hot = np.array(list(map(lambda cat: 1 if cat == category else 0, categories)))
    prediction_data = np.append(np.array([quantity, age, gender, price]), one_hot)
    logger.info(prediction_data)
    return prediction_data.reshape(1, -1)


def getOrderInfo(request):
    user = CustomUser.objects.get(username=request.user)
    orders = user.order_set.all()
    carts = Cart.objects.filter(order__in=orders).prefetch_related()
    full_price = 0
    quantity = 0
    categories = { key : 0 for key in ['tablets', 'phones', 'headphones', 'sdcards', 'covers', 'cables'] }
    for cart in carts:
        full_price += cart.quantity * cart.item.price
        quantity += cart.quantity
        categories[cart.item.category] += 1
    key = max(categories, key=lambda k: categories[k])
    category = str.upper(key[0]) + key[1:]
    path = apps.get_app_config('cart').path + '\\model.pkl'
    loaded_model = pickle.load(open(path, 'rb'))
    data = getPredictionData(full_price, quantity, user.gender, user.age, category)
    prediction = loaded_model.predict(data)
    logger.info(prediction)
    existance = ProfitUser.objects.filter(user=user)
    if existance.count() != 0:
        for user in existance:
            user.price = int(full_price)
            user.category = category
            user.save()
    if prediction[0]:
        if existance.count() == 0:
            ProfitUser.objects.create(user=user, price=int(full_price), category=category)


@method_decorator(login_required, name='dispatch')
class CheckoutSumbitedView(View):
    template_name = 'cart/checkout_submit.html'

    def get(self, request):
        cart_list = request.session.get('cart_list')
        if cart_list is not None:
            order = Order.objects.create(
                user=request.user, date=datetime.datetime.now(), status='Запрос отправлен')
            for key in cart_list:
                Cart.objects.create(item=ShopItem.objects.get(
                    id=key), quantity=cart_list[key], order=order)
            del request.session['cart_list']
            getOrderInfo(request)
            return render(request, self.template_name)
        else:
            return HttpResponseRedirect(reverse('items_view'))


def getDiscount(request):
    code = json.loads(request.body)
    response = Discount.objects.filter(code=code).values('code', 'amount')
    return HttpResponse(json.dumps(list(response), cls=DjangoJSONEncoder), content_type="application/json")
