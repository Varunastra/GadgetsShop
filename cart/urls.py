from django.urls import path
from .views import add_to_cart, get_cart, remove_from_cart, clear_session, CheckoutView, CheckoutSumbitedView, getDiscount


urlpatterns = [
    path('add-to-cart', add_to_cart, name='cart_add'),
    path('get-cart', get_cart, name="cart"),
    path('remove-cart', remove_from_cart, name="cart_remove"),
    path('clear-session', clear_session, name="session"),
    path('checkout', CheckoutView.as_view(), name="checkout"),
    path('checkout-submit', CheckoutSumbitedView.as_view(), name="checkout_submit"),
    path('discount-submit', getDiscount, name="discount_submit"),
]