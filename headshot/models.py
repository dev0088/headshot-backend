import os
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from djmoney.models.fields import MoneyField
from quantity.models import Quantity

STATUS_CHOICES = (
    ('Draft', 'Draft'),
    ('Requested', 'Requested'),
    ('Reviewing', 'Reviewing'),
    ('In Progress', 'In Progress'),
    ('Accepted', 'Accepted'),
    ('Declined', 'Declined'),
    ('Canceled', 'Canceled'),
    ('Completed', 'Completed'),
)


class Headshot(models.Model):
  email = models.CharField(max_length = 255, blank=True,  default='')
  file_name = models.CharField(max_length = 255)
  cloudinary_image_url = models.URLField(blank=True)
  cloudinary_image_secure_url = models.URLField(blank=True)
  quantity = models.ForeignKey(Quantity, related_name='quantity_headshots', on_delete=models.CASCADE, null=False, blank=False)
  status = models.CharField(choices=STATUS_CHOICES, default='Draft', max_length=20)
  public_id = models.CharField(max_length = 255, default='', blank=True)
  signature = models.CharField(max_length = 255, default='', blank=True)
  image_format = models.CharField(max_length = 10, default='', blank=True)
  width = models.IntegerField(default=400, blank=True)
  height = models.IntegerField(default=500, blank=True)
  doc_public_id = models.CharField(max_length = 255, default='', blank=True)
  doc_signature = models.CharField(max_length = 255, default='', blank=True)
  doc_format = models.CharField(max_length = 255, default='', blank=True)
  doc_size = models.IntegerField(default=0, blank=True)
  doc_url = models.URLField(blank=True)
  doc_secure_url = models.URLField(blank=True)
  doc_preview_url = models.URLField(blank=True)
  doc_preview_secure_url = models.URLField(blank=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def image_url(self):
    return self.cloudinary_image_url

  def image_tag(self):
      return mark_safe('<img src="{src}" width="{width}" height="{height}" />'.format(
                src=self.cloudinary_image_url, 
                width=150,
                height='auto'
            ))

  image_tag.short_description = 'Cloudinary Image'

  def __str__(self):
    return self.email + ': ' + self.file_name

  class Meta:
    db_table = "headshot"
    ordering = ('id', 'updated_at', 'email', 'file_name')
    unique_together = ('id', )
    managed = True