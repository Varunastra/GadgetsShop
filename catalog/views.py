from django.shortcuts import render
from catalog.models import Phone, Tablet, ShopItem, Cover, Cable, Sdcard, Headphone, Device, Accessorie
from django.views.generic import DetailView, ListView, View
from django.forms.models import model_to_dict
import logging
logger = logging.getLogger("mylogger")

# Create your views here.


class ItemListView(ListView):
    model = ShopItem
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        items = ShopItem.objects.all().order_by('-clicks')[:6]
        context = {'object_list': items}
        return context


class ItemView(DetailView):
    model = ShopItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = context['object']
        category = str.upper(item.category[:1]) + item.category[1:-1]
        item.clicks += 1
        item.save() 
        class_name = globals()[category]
        class_object = class_name.objects.get(slug=item.slug)
        self.model = class_name
        self.template_name = 'catalog/' + item.category[:-1] + '_detail.html'
        # object_with_titles = model_to_dict(class_object, fields=[field.verbose_name for field in class_object._meta.fields])
        # logger.info(object_with_titles)
        context['object'] = class_object
        return context


# class PhoneView(ItemView):
#     model = Phone


# class TabletView(ItemView):
#     model = Tablet


class PhonesView(ListView):
    model = Phone
    template_name = "catalog/categories/devices.html"


class TabletsView(ListView):
    model = Tablet
    template_name = "catalog/categories/tablets.html"


class CoversView(ListView):
    model = Cover
    template_name = "catalog/categories/covers.html"


class SdcardsView(ListView):
    model = Sdcard
    template_name = "catalog/categories/sdcards.html"


class CablesView(ListView):
    model = Cable
    template_name = "catalog/categories/cables.html"


class HeadphonesView(ListView):
    model = Headphone
    template_name = "catalog/categories/headphones.html"


class SearchView(View):
    template_name = "catalog/search.html"

    def get(self, request):
        query = request.GET['title']
        category = request.GET['category_name']
        if category == "":
            data = ShopItem.objects.all()
        else:
            first_filter = first_filter = ShopItem.objects.filter(category=category)
            data = first_filter.filter(title__icontains=query)
        return render(request, self.template_name, context={'object_list': data})


def FiltredItems(request, category, prop):
    template_name = 'catalog/categories/' + category + '.html'
    prop = prop.split('=')
    prop = { prop[0] : prop[1] }
    category = str.upper(category[:1]) + category[1:-1]
    data = {'object_list': globals()[category].objects.filter(**prop)}
    return render(request, template_name, data) 


def ItemsByPrice(request, category):
    template_name = 'catalog/categories/' + category + '.html'
    minim, maxim = (request.GET['min'],  request.GET['max'])
    category = str.upper(category[:1]) + category[1:-1]
    data = globals()[category].objects.filter(price__range=[minim, maxim])
    return render(request, template_name, context={'object_list': data})
    

def SortBySomething(request, category, prop):
    template_name = 'catalog/categories/' + category + '.html'
    category = str.upper(category[:1]) + category[1:-1]
    data = globals()[category].objects.all().order_by(prop)
    return render(request, template_name, context={'object_list': data})