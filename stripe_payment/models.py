import os
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from djmoney.models.fields import MoneyField
from headshot.models import Headshot

class StripePayment(models.Model):
  headshot = models.ForeignKey(Headshot, related_name='headshot_strype_payments', on_delete=models.CASCADE, null=False, blank=False)
  amount = models.FloatField(blank=True,  default=0.0)
  currency = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
  source = models.CharField(max_length = 255, default='', blank=True)
  description = models.TextField(max_length = 255, default='', blank=True)
  statement_descriptor = models.TextField(max_length = 255, default='', blank=True)
  order_id = models.IntegerField(blank=True,  default=0)
  customer_id = models.CharField(max_length = 255, default='', blank=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  token_id = models.CharField(max_length = 255, default='', blank=True)
  card_id = models.CharField(max_length = 255, default='', blank=True)
  # object_type = models.CharField(max_length = 100, default='', blank=True)
  address_city = models.CharField(max_length = 100, default='', blank=True)
  address_country = models.CharField(max_length = 100, default='', blank=True)
  address_line1 = models.CharField(max_length = 100, default='', blank=True)
  address_line1_check = models.CharField(max_length = 20, default='', blank=True)
  address_line2 = models.CharField(max_length = 20, default='', blank=True)
  address_state = models.CharField(max_length = 20, default='', blank=True)
  address_zip = models.CharField(max_length = 10, default='', blank=True)
  address_zip_check = models.CharField(max_length = 20, default='', blank=True)
  brand = models.CharField(max_length = 20, default='', blank=True)
  exp_month = models.IntegerField(blank=True,  default=0)
  exp_year = models.IntegerField(blank=True,  default=0)
  last4 = models.CharField(max_length = 4, default='', blank=True)
  livemode = models.BooleanField(default=False, blank=True)
  
  def __str__(self):
    return '{email}: {token}: ${amount}'.format(
      email=self.headshot.email,
      token=self.customer_id,
      amount=self.amount
    )

  class Meta:
    db_table = "stripe_payment"
    ordering = ('id', 'updated_at', 'headshot', 'order_id')
    unique_together = ('id', )
    managed = True