# todos/models.py
from django.db import models
from .utils import encrypt_text, decrypt_text


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Todo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    category = models.ForeignKey("Category", null=True, blank=True, on_delete=models.SET_NULL)
    encrypted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.encrypted and self.description:
            try:
                decrypt_text(self.description)
            except Exception:
                self.description = encrypt_text(self.description)
        super().save(*args, **kwargs)