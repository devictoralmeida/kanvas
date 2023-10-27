from django.urls import path

from contents.views import CreateContentView, RetrieveUpdateDestroyContentView

urlpatterns = [
    path(
        "courses/<uuid:course_id>/contents/",
        CreateContentView.as_view(),
    ),
    path(
        "courses/<uuid:course_id>/contents/<uuid:content_id>/",
        RetrieveUpdateDestroyContentView.as_view(),
    ),
]
