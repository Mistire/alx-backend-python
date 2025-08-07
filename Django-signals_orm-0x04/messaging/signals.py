from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

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
        # This is a new message; skip logging
        return

    try:
        original = Message.objects.get(id=instance.id)
    except Message.DoesNotExist:
        return 

    if original.content != instance.content:
        # Content has changed – log the edit
        MessageHistory.objects.create(
            message=original,
            old_content=original.content
        )
        instance.edited = True 