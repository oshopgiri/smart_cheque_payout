from django.db import models
from django.urls import reverse


class User(models.Model):
    name = models.CharField(max_length=254)
    email = models.EmailField(unique=True, null=False, blank=False)
    contact_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=254)
    state = models.CharField(max_length=254)
    zip = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user_edit', kwargs={'pk': self.pk})

    class Meta:
        app_label = 'app'
        db_table = 'user'
