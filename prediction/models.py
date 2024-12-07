from django.db import models


class Prediction(models.Model):
    uploaded_image = models.ImageField(upload_to='images/')
    result = models.CharField(max_length=50, blank=True, null=True)  # Result will store "Malignant" or "Benign"

    def __str__(self):
        return self.result if self.result else "No Prediction"
