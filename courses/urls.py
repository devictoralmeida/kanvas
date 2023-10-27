from django.urls import path
from courses.views import (
    ListCreateCourseView,
    RetrieveUpdateDestroyCourseView,
    RetrieveUpdateStudentView,
)

urlpatterns = [
    path("courses/", ListCreateCourseView.as_view()),
    path(
        "courses/<uuid:course_id>/", RetrieveUpdateDestroyCourseView.as_view()
    ),
    path(
        "courses/<uuid:course_id>/students/",
        RetrieveUpdateStudentView.as_view(),
    ),
]
