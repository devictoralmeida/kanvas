from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from accounts.models import Account
from accounts.permissions import IsAdminOrGetPermission, IsSuperUser
from courses.models import Course
from courses.serializers import CourseSerializer, CourseStudentSerializer
from students_courses.models import StudentCourse
from drf_spectacular.utils import extend_schema


class ListCreateCourseView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrGetPermission]
    serializer_class = CourseSerializer

    def get_queryset(self) -> Course:
        if self.request.user.is_superuser:
            return Course.objects.all()
        return Course.objects.filter(students=self.request.user.id)

    def perform_create(self, serializer):
        if "instructor" in serializer.validated_data:
            serializer.save(instructor=serializer.validated_data["instructor"])
        else:
            serializer.save()

    @extend_schema(
        description="Rota para criação de curso",
        tags=["Criação e listagem de curso"],
        parameters=[
            CourseSerializer,
        ],
    )
    def post(self, request):
        return self.create(request)

    @extend_schema(
        description="Rota para listagem de curso",
        tags=["Criação e listagem de curso"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveUpdateDestroyCourseView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrGetPermission]
    serializer_class = CourseSerializer
    lookup_url_kwarg = "course_id"

    def get_queryset(self) -> Course:
        if self.request.user.is_superuser:
            return Course.objects.all()
        return Course.objects.filter(students=self.request.user.id)

    @extend_schema(
        description="Rota para listagem de curso por ID",
        tags=["Listagem, atualização e deleção de curso"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Rota para atualização de curso por ID",
        tags=["Listagem, atualização e deleção de curso"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Rota para deleção de curso por ID",
        tags=["Listagem, atualização e deleção de curso"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RetrieveUpdateStudentView(RetrieveUpdateAPIView):
    permission_classes = [IsSuperUser]
    queryset = Course.objects.all()
    serializer_class = CourseStudentSerializer
    lookup_url_kwarg = "course_id"

    def perform_update(self, serializer):
        emails = []
        students_courses = serializer.validated_data.pop("students_courses")
        email = students_courses[0]["student"]["email"]
        try:
            course = Course.objects.get(pk=self.kwargs["course_id"])
            student = Account.objects.get(email=email)
            StudentCourse.objects.create(course=course, student=student)
            course.students.add(student)
        except Account.DoesNotExist:
            emails.append(email)
        if len(emails) > 0:
            emails = ",".join(emails)
            error = f"No active accounts was found: {emails}."
            raise ValidationError({"detail": error})

    @extend_schema(
        description="Rota para listagem dos estudantes do curso",
        tags=["Listagem e matrícula de estudante"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Rota para adição de alunos ao curso",
        tags=["Listagem e matrícula de estudante"],
        parameters=[
            CourseStudentSerializer,
        ],
    )
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
