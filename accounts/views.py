from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import generic
from .forms import CustomUserCreationForm
from django.views.generic import ListView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from cart.views import transform_json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import logging
from cart.models import Cart
from .models import Order
import json
logger = logging.getLogger("mylogger")

# Create your views here.


def convert_json(orders):
    items = []
    for order in orders:
        cart = transform_json(json.loads(order.cart))
        json_order = {'status': order.status, 'cart': cart}
        items.append(json_order)
    return json.dumps(items)


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@method_decorator(login_required, name='dispatch')
class GetOrders(View):

    def get(self, request):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        data = convert_json(orders)
        return HttpResponse(data, content_type="application/json")


def ViewOrders(request):
    template_name = 'orders.html'
    data = {'object_list': Order.objects.filter(user=request.user)}
    return render(request, template_name, data)
