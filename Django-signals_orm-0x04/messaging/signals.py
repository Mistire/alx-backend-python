from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    if instance.id is None:
        return

    try:
        original = Message.objects.get(id=instance.id)
    except Message.DoesNotExist:
        return 

    if original.content != instance.content:
        MessageHistory.objects.create(
            message=original,
            old_content=original.content
        )
        instance.edited = True 


@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    # Messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()