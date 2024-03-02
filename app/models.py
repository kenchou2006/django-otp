from django.db import models

class OTPKey(models.Model):
    account_name = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=40)
    def __str__(self):
        return f"{self.account_name}"