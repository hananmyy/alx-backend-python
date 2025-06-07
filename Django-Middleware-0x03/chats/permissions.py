from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsParticipantOfConversation(BasePermission):
    """ Allows access only to authenticated users who are participants in a conversation """

    def has_permission(self, request, view):
        return request.user.is_authenticated  # Ensure user is logged in

    def has_object_permission(self, request, view, obj):
        # Only conversation participants can view, update, and delete messages
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in obj.participants.all()
        return request.user in obj.participants.all()