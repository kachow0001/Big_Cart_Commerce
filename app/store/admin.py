from typing import Any
from django.contrib import admin,messages
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html,urlencode
from .import models 
    
#implement SimpleInventory filter that returns product with <10 inventory 
class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
               
@admin.register(models.Product) 
 #class specifies how to view /customize list page   
class ProductAdmin(admin.ModelAdmin):
# Fields for Admin Page 
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug' : ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 20
    list_filter = [InventoryFilter, 'collection', 'last_update']
    
    # Define search_fields for ProductAdmin
    search_fields = ['title', 'description']  # Add the fields you want to search by

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    # define custom action to clear inventory in CustomerAdmin page
    @admin.action(description='Clear Inventory')
    def clear_inventory(self,request,queryset):
        count_updated= queryset.update(inventory=0)
        #call the method to show to user
        self.message_user(
            request,
            f'{count_updated} products were deleted successfully.',
            messages.ERROR    
        )
        
        
"""Set up Cutomer to  load  First and Last name for each cutsomer
 and order by Membership type
"""
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','orders_count']
    list_editable =['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']
    
    @admin.display(ordering='orders_count')
    def orders_count(self,customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({
                    'customer__id': str(customer.id)
               })
               )
        return format_html('<a href = "{}">{}</a>',url,customer.order_count)
    
        
    def get_queryset(self,request):
        return super().get_queryset(request).annotate(
            order_count = Count('order')
        )
        
#Create Tabinline class to useOrderItems in Order Page
class OrderItemInline(admin.TabularInline): 
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    
#Setting up order page, to look list of order for customers    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id','placed_at','customer']
    
#setting up Collection app in Admin and annote Product count value 
@admin.register(models.Collection)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields = ['title']
    
    @admin.display(ordering='product_count')
    def product_count(self, collection):
        # to get url from user,import reverse(app_model_page) of target
        url = (
            reverse('admin:store_product_changelist')
            +'?'
            + urlencode({
                'collection__id':str(collection.id)    
            }))
        return format_html('<a href = "{}">{}</a>',url,collection.product_count)
         
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )
    
    