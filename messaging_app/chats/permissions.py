from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own conversations or messages.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()
        return False

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
