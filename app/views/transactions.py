from django.shortcuts import render, redirect, get_object_or_404
from django import forms

import datetime

from app.models import Transaction
from app.models import User


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['cheque_maker', 'cheque_type', 'cheque_number', 'account_number', 'routing_number', 'date_of_issue',
                  'amount', 'transaction_fees']

    cheque_maker = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cheque_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cheque_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    routing_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_issue = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    transaction_fees = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


def show(request, pk, template_name='transactions/show.html'):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, template_name, {'object': transaction})


def create(request, template_name='transactions/form.html'):
    form = TransactionForm(request.POST or None)
    user_id = request.GET.get('user_id')
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = get_object_or_404(User, pk=user_id)
        transaction.save()
        return redirect(get_redirect_path(user_id))
    return render(request, template_name, {'form': form, 'user_id': user_id})


# def update(request, pk, template_name='transactions/form.html'):
#     transaction = get_object_or_404(Transaction, pk=pk)
#     form = TransactionForm(request.POST or None, instance=transaction)
#     user_id = request.GET.get('user_id')
#     if form.is_valid():
#         form.save()
#         return redirect(get_redirect_path(user_id))
#     return render(request, template_name, {'form': form})


# def destroy(request, pk, template_name='transactions/transaction_confirm_delete.html'):
#     transaction = get_object_or_404(Transaction, pk=pk)
#     user_id = request.GET.get('user_id')
#     if request.method == 'POST':
#         transaction.delete()
#         return redirect(get_redirect_path(user_id))
#     return render(request, template_name, {'object': transaction})

def today(request, template_name='transactions/index.html'):
    transactions = Transaction.objects.filter(created_at__range=[datetime.datetime.now(), datetime.datetime.now()])
    return render(request, template_name, {'objects': transactions})


def get_redirect_path(user_id):
    if user_id:
        return '/users/view/%s' % user_id
    else:
        return '/users'
