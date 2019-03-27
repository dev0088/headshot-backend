from django.contrib import admin
from .models import Headshot

# @admin.register(models.Headshot)
class HeadshotAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'file_name', 
        'image_tag', 'cloudinary_image_url', 
        'quantity_display', 'status', 
        'updated_at', 'created_at'
    )
    list_display_links = (
        'id', 'email', 'file_name', 
        'image_tag', 'cloudinary_image_url', 
        'quantity_display', 
        'status', 
        'updated_at', 
        'created_at'
    )
    
    list_per_page = 25
    # explicitly reference fields to be shown, note image_tag is read-only
    fields = ( 
      'email', 'file_name', 
      'image_tag', 'cloudinary_image_url', 'cloudinary_image_secure_url',
      'quantity', 'status', 
      'image_format', 'width', 'height', 
      'public_id', 'signature',
    )
    readonly_fields = (
      'image_tag', 
      'image_format', 
      'width', 'height', 
      'public_id', 'signature'
    )

    def quantity_display(self, obj):
      return '{quantity}'.format(quantity=obj.quantity)

    quantity_display.short_description = 'Quantity'

admin.site.register(Headshot, HeadshotAdmin)
