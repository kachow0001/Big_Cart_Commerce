from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product  
from tags.models import TaggedItem

# Register your models here.

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']  # Corrected the field name here
    model = TaggedItem
    
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]  # Corrected the field name here
    
admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
