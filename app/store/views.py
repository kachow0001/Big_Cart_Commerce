from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Product,Collection,Reviews
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer
from django.db.models import Count

#created Product viewet combines methods of mutiple class(create/update/reterive/delete)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer()
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    
    def delete(self,request,pk):
        # Retrieve the product by its ID
        product = get_object_or_404(Product, pk=id)
        #there can some items order items linked to products, if so,dont allow count is > 0 :
        if product.orderitems.count() >0:
            return Response({'error':'Product not allowed to be deleted because it is linked to order'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        #product = get_object_or_404(Product,pk=id) is deleted here
        product.delete()
        return Response (status = status.HTTP_204_NO_CONTENT)
                    
#Collection-viewsets(RetrieveUpdateDestroyCreateAPIView)              
        
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
             
    
    def delete(self,request,pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=id)
        if collection.products.count() >0:
            return Response({'error':'Product not allowed to be deleted because it is linked to order'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class ReviewViewSet(ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
         