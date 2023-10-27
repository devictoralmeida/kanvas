from django.db import models
import uuid


class StudentCourseStatus(models.TextChoices):
    PENDING = "pending"
    ACCEPTED = "accepted"


class StudentCourse(models.Model):
    class Meta:
        ordering = ("id",)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    status = models.CharField(
        choices=StudentCourseStatus.choices,
        default=StudentCourseStatus.PENDING,
    )

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="students_courses",
    )
    student = models.ForeignKey(
        "accounts.Account",
        on_delete=models.CASCADE,
        related_name="students_courses",
    )
