from django.db import models
import uuid


class Content(models.Model):
    class Meta:
        ordering = ("id",)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=150)
    video_url = models.URLField(max_length=200, null=True)
    content = models.TextField()
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="contents"
    )
