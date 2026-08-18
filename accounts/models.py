from django.db import models
from django.utils import timezone
import uuid

class InviteCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

    def __str__(self):
        return f"{self.email} — {'Used' if self.is_used else 'Valid'}"
