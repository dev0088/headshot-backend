from django.contrib import admin
from .models import StripePayment


# @admin.register(models.Quantity)
class StripePaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'headshot',
        'amount',
        'currency',
        'source',
        'description',
        'statement_descriptor',
        'order_id',
        'customer_id',
        'updated_at',
        'created_at',
    )
    
    list_display_links = (
        'id', 
        'headshot',
        'amount',
        'currency',
        'source',
        'description',
        'statement_descriptor',
        'order_id',
        'customer_id',
        'updated_at',
        'created_at',
    )

    list_per_page = 25

    fields = ( 
        'headshot',
        'amount',
        'currency',
        'source',
        'description',
        'statement_descriptor',
        'order_id',
        'customer_id',
      )

admin.site.register(StripePayment, StripePaymentAdmin)
