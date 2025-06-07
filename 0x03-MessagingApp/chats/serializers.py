from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'username', 'bio', 'profile_picture']


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'conversation', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        """ Ensure message body isn't empty """
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        """ Fetch messages related to this conversation """
        messages = obj.messages.all().order_by('sent_at')
        return MessageSerializer(messages, many=True).data