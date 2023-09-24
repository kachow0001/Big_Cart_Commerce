from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from .import views

router = SimpleRouter()
#Register viewset and   Router generate url pattern for viewset
#register takes two parameters(prefix and viewset name)
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)



urlpatterns = router.urls
