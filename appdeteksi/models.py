from django.db import models
from django.contrib.auth.models import User


class DetectionHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='detections/'
    )

    result = models.CharField(
        max_length=100
    )

    confidence = models.FloatField()

    gradcam_image = models.ImageField(
        upload_to='gradcam/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.result}"