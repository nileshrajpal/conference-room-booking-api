from rest_framework import permissions

#  Only the owner of an account can unbook a room booked by the account


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_admin


class IsSlotOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.booked_by.username == request.user.username or request.user.is_admin:
            return True
