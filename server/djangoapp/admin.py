from django.contrib import admin
from .models import *

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 0

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    class Meta: 
        model = CarMake

class DealerReviewlInline(admin.TabularInline):
    model = DealerReview
    extra = 0

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)
