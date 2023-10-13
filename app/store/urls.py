from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from .import views

#create router object
router = routers.DefaultRouter()
#Register viewset and   Router generate url pattern for viewset
#register takes two parameters(prefix and viewset name)
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet)

#implement Parent router- router takes 3 parameters(parentrouter,parentprefix,lookupfield)
products_router = routers.NestedDefaultRouter(router,'products',lookup='product')
#register child resource (prefix,viewset,basename)
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')
#combine urls of both routers
urlpatterns = router.urls + products_router.urls
