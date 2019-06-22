from django.urls import path
from .views import SignUp, ViewOrders, GetOrders


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('orders/', ViewOrders, name='orders'),
    path('get-orders/', GetOrders.as_view(), name='get_orders'),
]