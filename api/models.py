from django.db import models
from django.contrib.auth.models import User


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='contact_messages'
    )

    def __str__(self):
        return f"{self.name} — {self.email} ({self.created_at:%Y-%m-%d})"

    class Meta:
        ordering = ['-created_at']