import os
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from djmoney.models.fields import MoneyField
from production.models import Production

class Quantity(models.Model):
  production = models.ForeignKey(Production, related_name='production_quantities', on_delete=models.CASCADE, blank=False)
  amount = models.IntegerField(blank=False, default=1)
  plus_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
  description = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return '{amount} (+ {plus_price})'.format(
      amount=self.amount,
      plus_price=self.plus_price
    )

  def caption(self):
    return '{amount} (+ {plus_price})'.format(
      amount=self.amount,
      plus_price=self.plus_price
    )

  class Meta:
    db_table = "quantity"
    ordering = ('production', 'amount', 'plus_price')
    unique_together = ('production', 'amount', 'plus_price')
    managed = True