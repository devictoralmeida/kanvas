from rest_framework import permissions


class IsCourseStudentOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            and request.user in obj.course.students.all()
            or request.user.is_superuser
        )
