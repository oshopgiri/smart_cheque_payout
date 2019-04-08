from django.db import models
from django.urls import reverse

import os

from app.models import User


def directory_path(instance, filename):
    return 'users/{0}/documents/{1}/{2}'.format(instance.user.id, instance.id, filename)


class Document(models.Model):
    name = models.CharField(max_length=254)
    attachment = models.FileField(upload_to=directory_path, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id is None:
            attachment = self.attachment
            self.attachment = None
            super(Document, self).save(*args, **kwargs)
            self.attachment = attachment
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        super(Document, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('document_edit', kwargs={'pk': self.pk})

    def attachment_name(self):
        return os.path.basename(self.attachment.name)

    class Meta:
        app_label = 'app'
        db_table = 'document'
