from django.db import models

# Create your models here.

class DiscordWebhook(models.Model):
    TYPE_CHOICES = (
        ("0", "Contest Notification"),
        ("1", "Job Notification"),
        ("2", "Hackathon Notification"),
    )

    username = models.CharField(max_length=16)
    webhook_id = models.CharField(max_length=32)
    webhook_token = models.CharField(max_length=128)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def __str__(self):
        return self.username