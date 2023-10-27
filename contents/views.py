from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSuperUser
from contents.models import Content
from contents.permissions import IsCourseStudentOwnerOrAdmin
from contents.serializers import ContentSerializer
from courses.models import Course
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema


class CreateContentView(CreateAPIView):
    permission_classes = [IsSuperUser]
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_url_kwarg = "course_id"

    @extend_schema(
        description="Rota para criação de conteúdo para um curso",
        tags=["Criação de conteúdos"],
        parameters=[
            ContentSerializer,
        ],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs["course_id"])
        serializer.save(course=course)


class RetrieveUpdateDestroyContentView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsCourseStudentOwnerOrAdmin]
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    lookup_url_kwarg = "content_id"

    def get_object(self):
        try:
            Course.objects.get(id=self.kwargs["course_id"])
            content = Content.objects.get(id=self.kwargs["content_id"])
        except Content.DoesNotExist:
            error = {"detail": "content not found."}
            raise NotFound(error)
        except Course.DoesNotExist:
            error = {"detail": "course not found."}
            raise NotFound(error)
        self.check_object_permissions(self.request, content)
        print(f"Students: {content.course.students}")
        return content

    @extend_schema(
        description="Rota para listagem de conteúdo por ID",
        tags=["Listagem, atualização e deleção de conteúdo"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Rota para atualização de conteúdo por ID",
        tags=["Listagem, atualização e deleção de conteúdo"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Rota para deleção de conteúdo por ID",
        tags=["Listagem, atualização e deleção de conteúdo"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
