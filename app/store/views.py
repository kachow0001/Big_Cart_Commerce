from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer
from django.db.models import Count

#create api_view decorator and apply to view func and replace http response with Response
@api_view(['GET','POST'])
def product_list(request):
    if request.method == "GET":
        queryset = Product.objects.select_related('collection').all()
        # Serialize the queryset (list of products) many=true helps queryset to  iterate Prod obj
        serializer = ProductSerializer(queryset,many=True,context={'request':request})
        return Response (serializer.data)
    
    elif request.method == "POST":
        #deserializer the body of obj(data=request.data)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
                
    """When Product doesn't have matching id in db records should show: 4040 error 
   using - get_object_or_404 wraps Try and Except in a block avoids 
   repetition of code
    """
      
#implementing product_details endpoint
@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    product = get_object_or_404(Product,pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
        
    elif request.method == 'PUT':
        #Not only deserializer  update instance of product and its attributes
        serializer = ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        #there can some items order items linked to products, if so,dont allow count is > 0 :
        if product.orderitems.count() >0:
            return Response({'error':'Product not allowed to be deleted because it is linked to order'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        #product = get_object_or_404(Product,pk=id) is deleted here
        product.delete()
        return Response (status = status.HTTP_204_NO_CONTENT)
           
        
@api_view(['GET','POST'])    
def collection_list(request):
    if request.method == 'GET':
        collection_query = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(collection_query,many=True)
        return Response(serializer.data)
     
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    
@api_view(['GET','PUT','DELETE'])
def collection_detail(request,id):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=id)
    if request.method =='GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection,data =request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    elif request.method == 'DELETE' :
        if collection.products.count() >0:
            return Response({'error':'Product not allowed to be deleted because it is linked to order'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
         
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        