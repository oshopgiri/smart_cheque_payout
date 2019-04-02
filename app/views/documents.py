from django.shortcuts import render, redirect, get_object_or_404
from django import forms

from app.models import Document
from app.models import User


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'attachment']

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    attachment = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))


def create(request, template_name='documents/form.html'):
    form = DocumentForm(request.POST or None, request.FILES)
    user_id = request.GET.get('user_id')
    if form.is_valid():
        document = form.save(commit=False)
        document.user = get_object_or_404(User, pk=user_id)
        document.save()
        return redirect(get_redirect_path(user_id))
    return render(request, template_name, {'form': form, 'user_id': user_id})


# def update(request, pk, template_name='documents/form.html'):
#     document = get_object_or_404(Document, pk=pk)
#     form = DocumentForm(request.POST or None, instance=document)
#     user_id = request.GET.get('user_id')
#     if form.is_valid():
#         form.save()
#         return redirect(get_redirect_path(user_id))
#     return render(request, template_name, {'form': form})


# def destroy(request, pk, template_name='documents/document_confirm_delete.html'):
#     document = get_object_or_404(Document, pk=pk)
#     user_id = request.GET.get('user_id')
#     if request.method == 'POST':
#         document.delete()
#         return redirect(get_redirect_path(user_id))
#     return render(request, template_name, {'object': document})

def get_redirect_path(user_id):
    if user_id:
        return '/users/view/%s' % user_id
    else:
        return '/users'
