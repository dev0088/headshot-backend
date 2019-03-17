from django.contrib import admin
from .models import Production

# @admin.register(models.Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'title', 'gallery_image_tag', 'gallery_image_external_url', 'overview_image_tag', 'overview_image_external_url', 'price', 'created_at'
    )
    list_display_links = (
        'id', 'name', 'title', 'gallery_image_tag', 'gallery_image_external_url', 'overview_image_tag', 'overview_image_external_url', 'price', 'created_at'
    )
    list_per_page = 25
    # explicitly reference fields to be shown, note image_tag is read-only
    fields = ( 
        'name', 'title', 'description', 'gallery_image_tag', 'gallery_image','gallery_image_external_url', 'overview_image_tag', 'overview_image', 'overview_image_external_url',
        'price', 'more_about'
      )
    readonly_fields = ('gallery_image_tag', 'overview_image_tag')


admin.site.register(Production, ProductionAdmin)