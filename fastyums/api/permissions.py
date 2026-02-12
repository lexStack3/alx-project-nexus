from django.contrib.auth import get_user_model
from rest_framework.permissions import (
    BasePermission, SAFE_METHODS
)

from accounts.models import User, Address


User = get_user_model()



class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsOwner(BasePermission):
    """
    Allows access to the owner of an object.
    """
    message = "Anonymous users are not allowed to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        owner = None

        if isinstance(obj, User):
            return request.user == obj or request.user.is_staff

        if hasattr(obj, 'owner'):
            owner = obj.owner
        elif hasattr(obj, 'user'):
            owner = obj.user
        elif hasattr(obj, 'order'):
            owner = obj.order.user
        elif isinstance(obj, Address):
            if isinstance(obj.content_object, User):
                owner = obj.content_object
            elif isinstance(obj.content_object, Vendor):
                owner = obj.content_object.owner

        return request.user == owner


class IsVendor(BasePermission):
    """
    Allows access to only users with role 'VENDOR'.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == User.Roles.VENDOR
        )


class IsCourier(BasePermission):
    """
    Allows access to only user with role 'CUORIER'.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == User.Role.COURIER
        )


class IsCustomer(BasePermission):
    """
    Allows access to only user with role 'CUSTOMER'.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == User.Role.CUSTOMER
        )


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
