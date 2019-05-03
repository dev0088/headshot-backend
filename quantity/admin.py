from django.contrib import admin
from .models import Quantity


# @admin.register(models.Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'production_display', 'amount', 'plus_price', 'description', 'created_at'
    )
    list_display_links = (
        'id', 'production_display', 'amount', 'plus_price', 'description', 'created_at'
    )
    list_per_page = 25
    fields = ( 
        'production', 'amount', 'plus_price', 'description'
      )

    def production_display(self, obj):
          return '{production_name}'.format(
              production_name=obj.production.name if obj.production else ''
          )

    production_display.short_description = 'Production'


admin.site.register(Quantity, QuantityAdmin)
