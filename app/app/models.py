import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Entry table
class Note(models.Model):
    # Sets a unique string as the ID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    # No character limit for the content
    content = models.TextField(blank=True, null=True)
    isFav = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # This is used to customise the way,
    # an entry record displays in the admin panel
    def __str__(self):
        return self.id
