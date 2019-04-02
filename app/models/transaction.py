from django.db import models
from django.urls import reverse

from app.models import User


class Transaction(models.Model):
    cheque_maker = models.CharField(max_length=254)
    cheque_type = models.CharField(max_length=254)
    cheque_number = models.CharField(max_length=254)
    account_number = models.CharField(max_length=254)
    routing_number = models.CharField(max_length=254)
    date_of_issue = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_fees = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.cheque_number

    def get_absolute_url(self):
        return reverse('transaction_edit', kwargs={'pk': self.pk})

    class Meta:
        app_label = 'app'
        db_table = 'transaction'
