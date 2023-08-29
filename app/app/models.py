import uuid
from django.db import models
from django.utils import timezone


# Entry table
class Entry(models.Model):
    # Sets a unique string as the ID
    entry_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    # No character limit for the content
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    # This is used to customise the way,
    # an entry record displays in the admin panel
    def __str__(self):
        return self.entry_id
