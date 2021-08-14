from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from creatorplatform.views import ProductView, StoreView, CategoryView, ReviewView, CustomerView

route = routers.DefaultRouter()

route.register("products", ProductView, basename='productview')
route.register("shops", StoreView, basename='storeview')
route.register("category", CategoryView, basename='categoryview')
route.register("reviews", ReviewView, basename='reviewview')
route.register("customers", CustomerView, basename='customerview')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(route.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

