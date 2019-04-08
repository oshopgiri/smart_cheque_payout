from django.shortcuts import render, redirect, get_object_or_404
from django import forms

import subprocess

from app.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'email', 'contact_number', 'date_of_birth', 'address', 'state', 'city', 'zip']

    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'accept': ".jpg,.jpeg,.png"}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contact_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


def index(request, template_name='users/index.html'):
    users = User.objects.all()
    data = {'object_list': users}
    return render(request, template_name, data)


def show(request, pk, template_name='users/show.html'):
    user = get_object_or_404(User, pk=pk)
    return render(request, template_name, {'object': user})


def create(request, template_name='users/form.html'):
    form = UserForm(request.POST or None, request.FILES)
    if form.is_valid():
        user = form.save()
        return redirect('user_view', pk=user.id)
    return render(request, template_name, {'form': form})


def update(request, pk, template_name='users/form.html'):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('user_view', pk=pk)
    return render(request, template_name, {'form': form})


def destroy(request, pk, template_name='users/confirm_delete.html'):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, template_name, {'object': user})


def detect(request, template_name='users/index.html'):
    subprocess.call(["python", "detect.py"])
    return redirect('user_list')
