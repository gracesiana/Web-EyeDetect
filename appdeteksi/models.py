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


class DatasetSample(models.Model):
    source_file = models.ImageField(
        upload_to='dataset_uploads/'
    )

    label = models.CharField(
        max_length=100
    )

    pattern = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.label} - {self.source_file.name}"