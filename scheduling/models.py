from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.service} on {self.date}"
