from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class UpdateProfile(BasePermission):
    """Allow user to edit only their own profile"""

    def has_object_permission(self, request: Request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # if the user tries to make a put object then we need this check
        # check if the obj we are updating matches the id of user of the request
        return obj.id == request.user.id
