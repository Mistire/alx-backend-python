from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own conversations or messages.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Allow only authenticated users.
    - Allow only participants of the conversation to GET, PUT, PATCH, DELETE.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method


        if hasattr(obj, 'participants'):
            is_participant = user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            is_participant = user in obj.conversation.participants.all()
        else:
            return False

        if method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return is_participant

      
        return True
