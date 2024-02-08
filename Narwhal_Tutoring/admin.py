from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(TimeSlot)
admin.site.register(Subject)
admin.site.register(Availability)
admin.site.register(Cart)
admin.site.register(Lesson)

class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0
 
 
class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]
 
 
admin.site.register(Product, ProductAdmin)