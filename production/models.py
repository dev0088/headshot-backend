import os
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from djmoney.models.fields import MoneyField


class Production(models.Model):
  name = models.CharField(max_length = 255)
  title = models.CharField(max_length = 255)
  description = models.TextField(blank=True)
  gallery_image = models.ImageField(upload_to='production', blank=True)
  gallery_image_external_url = models.URLField(blank=True)
  overview_image = models.ImageField(upload_to='production', blank=True)
  overview_image_external_url = models.URLField(blank=True)
  price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
  more_about = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def gallery_image_url(self):
      # returns a URL for either internal stored or external image url
      if self.gallery_image_external_url:
          return self.gallery_image_external_url
      else:
          return os.path.join('/', settings.MEDIA_URL, 'production/', os.path.basename(str(self.gallery_image)))

  def gallery_image_tag(self):
      return mark_safe('<img src="{src}" width="{width}" height="{height}" />'.format(
                src=self.gallery_image_url(), 
                width=150,
                height=(150 / self.gallery_image.width * self.gallery_image.height) if self.gallery_image else 150
            ))

  def overview_image_url(self):
      # returns a URL for either internal stored or external image url
      if self.overview_image_external_url:
          return self.overview_image_external_url
      else:
          return os.path.join('/', settings.MEDIA_URL, 'production/', os.path.basename(str(self.overview_image)))

  def overview_image_tag(self):
      return mark_safe('<img src="{src}" width="{width}" height="{height}" />'.format(
                src=self.overview_image_url(), 
                width=150,
                height=(150 / self.overview_image.width * self.overview_image.height) if self.overview_image else 150
            ))


  gallery_image_tag.short_description = 'Gallery Image'
  overview_image_tag.short_description = 'Overview Image'  

  def __str__(self):
    return self.title

  class Meta:
    db_table = "production"
    ordering = ('id', 'name', 'title')
    unique_together = ('name', )
    managed = True