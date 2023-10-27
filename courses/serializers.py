from rest_framework import serializers
from contents.serializers import ContentSerializer
from students_courses.serializers import StudentCourseSerializer
from .models import Course, CourseStatus


class CourseSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    students_courses = StudentCourseSerializer(many=True, read_only=True)
    status = serializers.ChoiceField(
        choices=CourseStatus.choices, required=False
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "status",
            "name",
            "start_date",
            "end_date",
            "contents",
            "instructor",
            "students_courses",
        ]


class CourseStudentSerializer(serializers.ModelSerializer):
    students_courses = StudentCourseSerializer(many=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "students_courses"]
