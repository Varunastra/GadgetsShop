from django.urls import path
from catalog.views import *


urlpatterns = [
    path('', ItemListView.as_view(), name='items_view'),
    path('phones/<slug>', ItemView.as_view(), name='phone_detail'),
    path('tablets/<slug>', ItemView.as_view(), name='tablet_detail'),
    path('headphones/<slug>', ItemView.as_view(), name='headphone_detail'),
    path('covers/<slug>', ItemView.as_view(), name='phone_detail'),
    path('sdcards/<slug>', ItemView.as_view(), name='sdcard_detail'),
    path('cables/<slug>', ItemView.as_view(), name='cables_detail'),
    path('phones', PhonesView.as_view(), name='phones_view'),
    path('tablets', TabletsView.as_view(), name='tablets_view'),
    path('covers', CoversView.as_view(), name='covers_view'),
    path('sdcards', SdcardsView.as_view(), name='sdcards_view'),
    path('headphones', HeadphonesView.as_view(), name='headphones_view'),
    path('cables', CablesView.as_view(), name='cables_view'),
    path('search', SearchView.as_view(), name='search_view'),
    path('<category>_filter_by_<prop>', FiltredItems, name='filtred_items_view'),
    path('<category>_filter_price', ItemsByPrice, name='price_items'),
    path('<category>/sort/by_<prop>', SortBySomething, name='sort_by_something'),
]   
