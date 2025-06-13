from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class NotificationSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='password123')
        self.receiver = User.objects.create_user(username='bob', password='password456')

    def test_notification_created_on_message_save(self):
        # Send a message from Alice to Bob
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hey Bob!"
        )

        # Check that a notification was created
        notification_exists = Notification.objects.filter(user=self.receiver, message=message).exists()
        self.assertTrue(notification_exists, "Notification should be created when a new message is sent.")