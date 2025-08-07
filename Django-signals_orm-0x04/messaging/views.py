from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('login')


def get_threaded_messages_for_user(user):
    root_messages = Message.objects.filter(sender=request.user, receiver=user, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
    return root_messages

def get_all_replies(message):
    replies = []

    def fetch_replies(parent):
        children = parent.replies.all().select_related('sender', 'receiver')
        for child in children:
            replies.append(child)
            fetch_replies(child)

    fetch_replies(message)
    return replies

def unread_messages_view(request):
    unread_messages = Message.unread.for_user(request.user)
