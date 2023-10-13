from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.response import Response
from .models import Product,Collection,Reviews,OrderItem,Cart
from .filters import ProductFilter
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer
from .pagination import DefaultPagination


#created Product views combines methods of mutiple class(create/update/reterive/delete)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    #specify name of fields to include for filtering-
    filterset_fields = ['collection_id','unit_price']
    filterset_class = ProductFilter
    pagination_class =DefaultPagination
    search_fields = ['collection', 'description']
    ordering_fields = ['unit_price']
    
    
    
    """
    filter-logic without importing filterBackend
    def get_queryset(self):
        queryset = Product.objects.all()
        # read collection_id from query strin
        #get method returns collection_id regardless of different collection_id name 
        collection_id = self.request.query_params.get('collection_id')
        
        if collection_id is not None:
            #apply filter get queryset and return to new updated queryset
            queryset = queryset.filter(collection_id = collection_id)  
            
        return queryset
    """
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    #Delete option is visible when passing Product id to endpoint :
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0 :
            return Response({'error':'Product not allowed to be deleted because it is linked to order'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)
    
    
#Collection-viewsets(RetrieveUpdateDestroyCreateAPIView)              
        
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
             
    
    def delete(self,request,pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
        if collection.products.count() >0:
            return Response({'error':'Product not allowed to be deleted because it is linked to order'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class ReviewViewSet(ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Reviews.objects.filter(product_id=self.kwargs['product_pk'])
    
    #context object is created to pass additional data to serializer:
    def get_serializer_context(self):
        #kwarg-library used to extract parameters from url,here it is returned in dictonary
        return {'product_id':self.kwargs['product_pk']}
                  
#to view cart id,details without exposing cart_id to client,implement customModelviews         
class CartViewSet(CreateModelMixin,GenericViewSet):
    queryset = Cart.objects.all()   
    serializer_class = CartSerializer
    
         