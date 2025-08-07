from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.shortcuts import render
from .models import Message
from django.views.decorators.cache import cache_page

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

@login_required
def unread_messages_view(request):
    unread_msgs_qs = Message.unread.unread_for_user(request.user)
    unread_msgs = unread_msgs_qs.only('id', 'sender', 'content', 'timestamp')
    return render(request, "messaging/unread_messages.html", {"messages": unread_msgs})

@cache_page(60)  
def conversation_messages_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
    return render(request, "chats/conversation.html", {"messages": messages})

@cache_page(60)
def message_list(request):
    messages = Message.objects.all()
    return render(request, "messages/message_list.html", {"messages": messages})
