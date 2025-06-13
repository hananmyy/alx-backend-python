from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def notify_receiver(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Means the message already exists
        previous = Message.objects.get(pk=instance.pk)
        if previous.content != instance.content:
            MessageHistory.objects.create(message=instance, old_content=previous.content)
            instance.edited = True


@receiver(post_delete, sender=User)
def clean_up_user_data(sender, instance, **kwargs):
    # This is mostly optional due to on_delete=CASCADE, but can be enforced explicitly
    Notification.objects.filter(user=instance).delete()
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
