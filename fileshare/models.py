from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings 
import uuid


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('OPS', 'Operations'),
        ('CLIENT', 'Client')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"

class SharedFile(models.Model):
    uploaded_by = models.ForeignKey(
    CustomUser,
    on_delete=models.CASCADE,
    related_name='files'
    )

    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.file.name
    
class FileDownloadToken(models.Model):
    file = models.ForeignKey('SharedFile', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)

