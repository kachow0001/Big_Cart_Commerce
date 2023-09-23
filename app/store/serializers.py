from decimal import Decimal
from rest_framework import serializers
from .models import Product,Collection

#create Collection serializers 
class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField() 

    class Meta:
        
        model = Collection
        fields = ['id','title','products_count']
        
    # Calculate products_count for the collection
    def get_products_count(self, collection):
        return collection.products.count()    
    
# Create serializers for converting a Product object into a Product Dict

class ProductSerializer(serializers.ModelSerializer):
    # Define a SerializerMethodField for price_with_tax
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    collection = CollectionSerializer()
    class Meta:
        model = Product
        fields = ['id','title','slug','description','inventory','unit_price','price_with_tax','collection']
        
    #for custom serializer field we are creating fun to cal Tax 
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(2.0)
        
        