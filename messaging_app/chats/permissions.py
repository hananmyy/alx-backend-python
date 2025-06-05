from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """ Allows access only to conversation participants """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()