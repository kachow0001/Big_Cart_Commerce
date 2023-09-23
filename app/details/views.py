from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product,OrderItem,Order

# Create your views here.

def first_display(request):
    query_set = Order.object.select_related('customer').prefetch_related('item').orderby()
        
    return render(request,'hello.html',{'name': 'kay','orders':list(query_set)})
