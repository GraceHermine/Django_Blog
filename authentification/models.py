import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils import timezone

class PasswordResetCode(models.Model):
    email = models.EmailField(null=True, blank=True) # Ce champ doit être présent pour recevoir l'email de l'utilisateur
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def is_valid(self):
        # Le code est valide s'il a moins de 5 minutes
        return (timezone.now() - self.created_at).total_seconds() < 300
