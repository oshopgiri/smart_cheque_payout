from django import forms
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

import base64
import subprocess

from app.models import User


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['avatar', 'avatar_base64', 'name', 'email', 'contact_number', 'date_of_birth', 'address', 'state',
		          'city', 'zip']

	avatar = forms.ImageField(required=False,
	                          widget=forms.FileInput(attrs={'class': 'form-control', 'accept': ".jpg,.jpeg,.png"}))
	avatar_base64 = forms.CharField(required=False, widget=forms.HiddenInput())
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
		user = form.save(commit=False)
		if not user.avatar:
			if form.data['avatar_base64']:
				format, image = form.data['avatar_base64'].split(';base64,')
				extension = format.split('/')[-1]
				user.avatar = ContentFile(base64.b64decode(image), name='temp.' + extension)
			else:
				form.add_error('avatar', 'This field is required.')
				return render(request, template_name, {'form': form})
		user.save()
		return redirect('user_view', pk=user.id)

	return render(request, template_name, {'form': form})


def update(request, pk, template_name='users/form.html'):
	user = get_object_or_404(User, pk=pk)
	form = UserForm(request.POST or None, request.FILES or None, instance=user)
	if form.is_valid():
		user = form.save(commit=False)
		if form.data['avatar_base64']:
			format, image = form.data['avatar_base64'].split(';base64,')
			extension = format.split('/')[-1]
			user.avatar = ContentFile(base64.b64decode(image), name='temp.' + extension)
		user.save()
		return redirect('user_view', pk=pk)
	return render(request, template_name, {'form': form})


def destroy(request, pk, template_name='users/confirm_delete.html'):
	user = get_object_or_404(User, pk=pk)
	if request.method == 'POST':
		user.delete()
		return redirect('user_list')
	return render(request, template_name, {'object': user})


def detect(request, template_name=''):
	result = subprocess.run(['python', 'detect.py'], stdout=subprocess.PIPE)
	pk = result.stdout.decode('utf-8')
	response = { 'success': False }
	if pk:
		response = { 'success': True, 'profile_url': reverse('user_view', args=[pk]) }

	return JsonResponse(response)
