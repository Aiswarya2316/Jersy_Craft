from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Product)
admin.site.register(cart)
admin.site.register(Buy)
admin.site.register(Category)
admin.site.register(Register)
admin.site.register(ProductImage)
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'rating', 'submitted_at')