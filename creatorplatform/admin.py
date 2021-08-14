from django.contrib import admin

# Register your models here.
from creatorplatform.models import Customer, Product, Store, Review, Category

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Store)
admin.site.register(Review)
admin.site.register(Category)
